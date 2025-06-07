from typing_extensions import Final

from non_planar_slicing_deformation.configuration.KeyValueParameters import KeyValueParameters

simpleDeformerDefaults: Final[KeyValueParameters] = KeyValueParameters({
    "radius": 0.0
    })
simpleUndeformerDefaults: Final[KeyValueParameters] = KeyValueParameters({})
