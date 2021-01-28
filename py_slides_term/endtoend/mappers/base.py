from __future__ import annotations
from abc import ABCMeta, abstractmethod
from typing import Dict, Union, Generic, TypeVar

MappedValue = TypeVar("MappedValue")


class BaseMapper(Generic[MappedValue], metaclass=ABCMeta):
    # public
    def __init__(self):
        self._map: Dict[str, MappedValue] = dict()

    def add(self, name: str, value: MappedValue):
        self._map[name] = value

    def find(self, name: str) -> Union[MappedValue, None]:
        return self._map.get(name)

    @classmethod
    @abstractmethod
    def default_mapper(cls) -> BaseMapper[MappedValue]:
        raise NotImplementedError(f"{cls.__name__}.default_mapper()")
