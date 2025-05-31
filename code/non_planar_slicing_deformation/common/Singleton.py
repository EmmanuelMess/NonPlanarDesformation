from __future__ import annotations

from typing_extensions import TypeVar, Generic, Any

_T = TypeVar("_T")


class Singleton(type, Generic[_T]):
    """
    A metaclass designed to hijack the constructor of the class to generate and always use a single instance
    """
    _instances: dict[Singleton[_T], _T] = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> _T:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
