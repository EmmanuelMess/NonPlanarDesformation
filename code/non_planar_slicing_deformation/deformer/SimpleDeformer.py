from typing_extensions import Optional, override

import numpy as np
import pyvista as pv

from non_planar_slicing_deformation.common.MainLogger import MAIN_LOGGER
from non_planar_slicing_deformation.configuration import Defaults
from non_planar_slicing_deformation.deformer.Deformer import Deformer


class SimpleDeformer(Deformer):
    def __init__(self):
        super().__init__(Defaults.simpleDeformerDefaults)

    @override
    def deformImplementation(self) -> Optional[pv.DataObject]:
        mesh = self.getMesh()

        if mesh is None:
            MAIN_LOGGER.error("Model is not set yet!")
            return None

        mesh = mesh.copy()
        mesh.field_data["faces"] = mesh.faces.reshape(-1, 4)[:, 1:]  # assume all triangles

        # scale mesh
        mesh.points *= 1

        # center around the middle of the bounding box
        xmin, xmax, ymin, ymax, zmin, zmax = mesh.bounds
        mesh.points -= np.array([(xmin + xmax) / 2, (ymin + ymax) / 2, zmin])
        # mesh.points -= np.array([0, 0, 0]) # optionally offset the part from the center

        mesh.points = mesh.points[:10]

        # max radius of part
        max_radius = np.max(np.linalg.norm(mesh.points[:, :2], axis=1))

        # define rotation as a function of radius
        ROTATION = lambda radius: self.getParameters()["radius", float] * (radius / max_radius)
        # ROTATION = lambda radius: np.deg2rad(15 + 30 * (radius / max_radius))  # Use for propeller and tree
        # ROTATION = lambda radius: np.full_like(radius, np.deg2rad(-40)) # Fixed rotation inwards
        # ROTATION = lambda radius: np.deg2rad(-40 + 30 * (1 - (radius / max_radius)) ** 2) # Use for bridge

        # rotate points around max diameter ring
        distances_to_center = np.linalg.norm(mesh.points[:, :2], axis=1)
        translate_upwards = np.hstack([np.zeros((len(mesh.points), 2)), np.tan(
            ROTATION(distances_to_center).reshape(-1, 1)) * distances_to_center.reshape(-1, 1)])

        mesh.points = mesh.points + translate_upwards

        # make bottom of part z=0 and center in bound box. remember the offsets for later
        xmin, xmax, ymin, ymax, zmin, zmax = mesh.bounds
        offsets_applied = np.array([(xmin + xmax) / 2, (ymin + ymax) / 2, zmin])
        mesh.points -= offsets_applied

        return mesh
