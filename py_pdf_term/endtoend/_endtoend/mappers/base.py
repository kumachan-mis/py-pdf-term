from __future__ import annotations

from abc import ABCMeta, abstractmethod
from typing import Dict, Generic, List, TypeVar, Union

MappedValue = TypeVar("MappedValue")


class BaseMapper(Generic[MappedValue], metaclass=ABCMeta):
    def __init__(self) -> None:
        self._map: Dict[str, MappedValue] = dict()

    def add(self, name: str, value: MappedValue) -> None:
        self._map[name] = value

    def remove(self, name: str) -> None:
        del self._map[name]

    def find(self, name: str) -> MappedValue:
        return self._map[name]

    def find_or_none(self, name: str) -> Union[MappedValue, None]:
        return self._map.get(name)

    def bulk_find(self, names: List[str]) -> List[MappedValue]:
        return list(map(lambda name: self._map[name], names))

    def bulk_find_or_none(self, names: List[str]) -> List[Union[MappedValue, None]]:
        return list(map(self._map.get, names))

    @classmethod
    @abstractmethod
    def default_mapper(cls) -> BaseMapper[MappedValue]:
        raise NotImplementedError(f"{cls.__name__}.default_mapper()")
