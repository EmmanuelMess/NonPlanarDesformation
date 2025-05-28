from typing_extensions import override, Optional, List

import numpy as np

import pygcode as pg

from common.MainLogger import MAIN_LOGGER
from configuration import Defaults
from configuration.CurrentDeformerState import CurrentDeformerState
from state.SimpleDeformerState import SimpleDeformerState
from undeformer.Undeformer import Undeformer


class SimpleUndeformer(Undeformer):
    def __init__(self):
        super().__init__(Defaults.simpleUndeformerDefaults)

        self.state: Optional[SimpleDeformerState] = None

    @override
    def undeformImplementation(self, gcode: List[str]) -> Optional[List[str]]:
        if CurrentDeformerState().getState() is None:
            MAIN_LOGGER.error("Missing state, did you forget to call CurrentDeformerState.setState?")
            return None

        state = CurrentDeformerState().getState()

        # TODO split this into functions

        # read gcode
        pos = np.array([0., 0., 20.])
        feed = 0
        gcode_points = []

        for line_text in gcode:
            line = pg.Line(line_text)

            extrusion = None

            move_command_seen = False

            if not line.block.gcodes:
                continue

            # extract position and feedrate
            for gcode in sorted(line.block.gcodes):
                if gcode.word == "G01" or gcode.word == "G00":
                    move_command_seen = True
                    prev_pos = pos.copy()

                    if gcode.X is not None:
                        pos[0] = gcode.X
                    if gcode.Y is not None:
                        pos[1] = gcode.Y
                    if gcode.Z is not None:
                        pos[2] = gcode.Z

                if gcode.word.letter == "F":
                    feed = gcode.word.value

            if not move_command_seen:
                continue

            # extract extrusion
            for param in line.block.modal_params:
                if param.letter == "E":
                    extrusion = param.value

            # segment moves
            # prevents G0 (rapid moves) from hitting the part
            # makes G1 (feed moves) less jittery
            delta_pos = pos - prev_pos
            distance = np.linalg.norm(delta_pos)
            if distance > 0 and gcode.word == "G01":
                seg_size = 1  # mm
                num_segments = -(-distance // seg_size)  # hacky round up
                seg_distance = distance / num_segments

                # calculate inverse time feed
                time_to_complete_move = (1 / feed) * seg_distance  # min/mm * mm = min
                if time_to_complete_move == 0:
                    inv_time_feed = None
                else:
                    inv_time_feed = 1 / time_to_complete_move  # 1/min

                for i in range(int(num_segments)):
                    gcode_points.append({
                        "position": (prev_pos + delta_pos * (i + 1) / num_segments) + state.offsetsApplied,
                        "command": gcode.word,
                        "extrusion": extrusion / num_segments if extrusion is not None else None,
                        "inv_time_feed": inv_time_feed,
                        "move_length": seg_distance,
                        "start_position": prev_pos,
                        "end_position": pos,
                        "unsegmented_move_length": distance
                    })
            else:
                gcode_points.append({
                    "position": pos.copy() + state.offsetsApplied,
                    "command": gcode.word,
                    "extrusion": extrusion,
                    "inv_time_feed": None,
                    "move_length": 0
                })

        # untransform gcode
        positions = np.array([point["position"] for point in gcode_points])
        distances_to_center = np.linalg.norm(positions[:, :2], axis=1)
        translate_upwards = np.hstack([np.zeros((len(positions), 2)), np.tan(
            state.rotation(distances_to_center).reshape(-1, 1)) * distances_to_center.reshape(-1, 1)])

        new_positions = positions - translate_upwards

        # cap travel move height to be just above the part and to not travel over the origin
        max_z = 0
        for i, point in enumerate(gcode_points):
            if point["command"] == "G01":
                max_z = max(max_z, new_positions[i][2])
        for i, point in enumerate(gcode_points):
            if point["command"] == "G00":
                if new_positions[i][2] > max_z:
                    new_positions[i] = None

        # rescale extrusion by change in move_length
        prev_pos = np.array([0., 0., 0.])
        for i, point in enumerate(gcode_points):
            if point["extrusion"] is not None and point["move_length"] != 0:
                extrusion_scale = np.linalg.norm(new_positions[i] - prev_pos) / point["move_length"]
                point["extrusion"] *= min(extrusion_scale, 10)
            prev_pos = new_positions[i]

        # rescale extrusion to compensate for rotation deformation
        distances_to_center = np.linalg.norm(new_positions[:, :2], axis=1)
        extrusion_scales = np.cos(state.rotation(distances_to_center))
        for i, point in enumerate(gcode_points):
            if point["extrusion"] is not None:
                point["extrusion"] *= extrusion_scales[i]

        NOZZLE_OFFSET = 43  # mm

        prev_r = 0
        prev_theta = 0
        prev_z = 20

        theta_accum = 0

        # save transformed gcode
        outputLines: List[str] = []
        # write header
        outputLines.append("G94 ; mm/min feed  ")
        outputLines.append("G28 ; home ")
        outputLines.append("M83 ; relative extrusion ")
        outputLines.append("G1 E10 ; prime extruder ")
        outputLines.append("G94 ; mm/min feed ")
        outputLines.append("G90 ; absolute positioning ")
        outputLines.append(f"G0 C{prev_theta} X{prev_r} Z{prev_z} B{-np.rad2deg(state.rotation(0))}")
        outputLines.append("G93 ; inverse time feed ")

        for i, point in enumerate(gcode_points):
            position = new_positions[i]

            if position is None:
                continue

            if np.all(np.isnan(position)):
                continue

            if position[2] < 0:
                continue

            #################################################################################################
            ### If you want to print on another type of 4 axis printer, you will need to change this code ###
            #################################################################################################
            # convert to polar coordinates
            r = np.linalg.norm(position[:2])
            theta = np.arctan2(position[1], position[0])
            z = position[2]

            rotation = state.rotation(r) * 1

            # compensate for nozzle offset
            r += np.sin(rotation) * NOZZLE_OFFSET
            z += (np.cos(rotation) - 1) * NOZZLE_OFFSET

            delta_theta = theta - prev_theta
            if delta_theta > np.pi:
                delta_theta -= 2 * np.pi
            if delta_theta < -np.pi:
                delta_theta += 2 * np.pi

            theta_accum += delta_theta

            string = f"{point['command']} C{np.rad2deg(theta_accum):.5f} X{r:.5f} Z{z:.5f} B{-np.rad2deg(rotation):.5f}"
            #################################################################################################
            ### If you want to print on another type of 4 axis printer, you will need to change this code ###
            #################################################################################################

            if point["extrusion"] is not None:
                string += f" E{point['extrusion']:.4f}"

            no_feed_value = False
            if point["inv_time_feed"] is not None:
                string += f" F{(point['inv_time_feed']):.4f}"
            else:
                string += f" F50000"
                outputLines.append(f"G94")
                no_feed_value = True

            outputLines.append(string)

            if no_feed_value:
                outputLines.append(f"G93")  # back to inv feed

            # update previous values
            prev_r = r
            prev_theta = theta
            prev_z = z

        return outputLines
