import re

import numpy as np
import pygcode as pg  # type: ignore
import pyvista as pv
from typing_extensions import Optional, List, Tuple


G_COMMAND_3_AXIS_GCODE_REGEX = re.compile(
    r"(?:G1|G0)\s?(?:F[\-\d.]+)?\s?X(?P<x_coord>[\-\d.]+)\s?"
    r"Y(?P<y_coord>[\-\d.]+)\s?(Z(?P<z_coord>[\-\d.]+))?\s?(?:E[\-\d.]+)?"
)

G_COMMAND_4_AXIS_GCODE_REGEX = re.compile(
    r"(?:G01|G00)\s?C(?P<c_coord>[\-\d.]+)\s?X(?P<x_coord>[\-\d.]+)\s?Z(?P<z_coord>[\-\d.]+)\s?"
    r"B(?P<b_coord>[\-\d.]+)\s?(?:E[\-\d.]+)?\s?(?:F[\-\d.]+)?"
)


def plottable3AxisGcode(lines: List[str]) -> Optional[pv.PolyData]:
    """
    Simple function to convert gcode lines to a pv.PolyData that can be plotted
    """

    # TODO check that is relative

    points: List[Tuple[np.float64, np.float64, np.float64]] = []

    x = np.float64(0)
    y = np.float64(0)
    z = np.float64(20)  # TODO check this

    for gcodeLine in lines:
        line = pg.Line(gcodeLine)
        if not line.block.gcodes:
            continue

        # extract position and feedrate
        for gcode in sorted(line.block.gcodes):
            if gcode.word in ["G01", "G00"]:
                if gcode.X is not None:
                    x = gcode.X
                if gcode.Y is not None:
                    y = gcode.Y
                if gcode.Z is not None:
                    z = gcode.Z

                # TODO check this
                points.append((x, y, z))

    pointArray = np.array(points)

    return pv.PolyData(pointArray)


def plottable4AxisGcode(lines: List[str]) -> Optional[pv.PolyData]:
    """
    Simple function to convert gcode lines to a pv.PolyData that can be plotted
    """

    # TODO check that is absolute

    points: List[Tuple[np.float64, np.float64, np.float64]] = []

    c = np.float64(0)
    x = np.float64(0)
    z = np.float64(0)

    for gcodeLine in lines:
        line = pg.Line(gcodeLine)
        if not line.block.gcodes:
            continue

        # extract position and feedrate
        for gcode in sorted(line.block.gcodes):
            if gcode.word in ["G01", "G00"]:
                if gcode.C is not None:
                    c = gcode.C
                if gcode.X is not None:
                    x = gcode.X
                if gcode.Z is not None:
                    z = gcode.Z

                cartesianX = np.cos(np.deg2rad(c)) * x
                cartesianY = np.sin(np.deg2rad(c)) * x
                cartesianZ = z

                # TODO check this
                points.append((cartesianX, cartesianY, cartesianZ))

    pointArray = np.array(points)

    return pv.PolyData(pointArray[pointArray[:, 2] > 0])
