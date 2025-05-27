from typing_extensions import Any, Set, Optional, Type, Dict, Tuple

from non_planar_slicing_deformation.common.MainLogger import MAIN_LOGGER


class KeyValueParameters:
    """
    Meant to be a generic way to pass parameters from a configurable UI to a Deformer or Underformer
    """

    def __init__(self, defaults: Dict[str, Any]) -> None:
        self.map = defaults

    def __getitem__(self, item: Tuple[str, Type[Any]]) -> Optional[Any]:
        key, type = item
        if key not in self.map.keys():
            MAIN_LOGGER.warn(f"Key {key} is not in parameter map {self.map}")
            return None

        if not isinstance(self.map[key], type):
            MAIN_LOGGER.warn(f"Value for '{key}' is not of type '{type}'")
            return None

        return self.map[key]

    def __setitem__(self, key: str, value: Any) -> None:
        if key not in self.map.keys():
            MAIN_LOGGER.warn(f"Key {key} is not in parameter map {self.map}, did you forget to set a default value?")

        self.map[key] = value