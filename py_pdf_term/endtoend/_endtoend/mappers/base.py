from __future__ import annotations

from abc import ABCMeta, abstractmethod


class BaseMapper[MappedValue](metaclass=ABCMeta):
    """Base class for mappers to find mapped values from names."""

    def __init__(self) -> None:
        self._map: dict[str, MappedValue] = dict()

    def add(self, name: str, value: MappedValue) -> None:
        """Add a new mapping from name to value.

        Args
        ----
            name:
                Name to find the mapped value.
            value:
                Mapped value to be found from the name.
        """

        self._map[name] = value

    def remove(self, name: str) -> None:
        """Remove a mapping from name to value.

        Args
        ----
            name:
                Name to remove the mapped value.
        """

        del self._map[name]

    def find(self, name: str) -> MappedValue:
        """Find a mapped value from name. If not found, raise KeyError.

        Args
        ----
            name:
                Name to find the mapped value.

        Returns
        -------
            Mapped value found from the name.
        """

        return self._map[name]

    def find_or_none(self, name: str) -> MappedValue | None:
        """Find a mapped value from name. If not found, return None.


        Args
        ----
            name:
                Name to find the mapped value.

        Returns
        -------
            Mapped value found from the name. None if not found.
        """

        return self._map.get(name)

    def bulk_find(self, names: list[str]) -> list[MappedValue]:
        """Find mapped values from names. If there is no mapped value for a name, raise
        KeyError.

        Args
        ----
            names:
                Names to find the mapped values.

        Returns
        -------
            Mapped values found from the names. The order of the mapped values is the
            same as the order of the names.
        """

        return list(map(lambda name: self._map[name], names))

    def bulk_find_or_none(self, names: list[str]) -> list[MappedValue | None]:
        """Find mapped values from names. If there is no mapped value for a name, return
        None.

        Args
        ----
            names:
                Names to find the mapped values.

        Returns
        -------
            Mapped values found from the names. The order of the mapped values is the
            same as the order of the names. None if there is no mapped value for a name.
        """

        return list(map(self._map.get, names))

    @classmethod
    @abstractmethod
    def default_mapper(cls) -> BaseMapper[MappedValue]:
        """Return a default mapper for this class."""

        raise NotImplementedError(f"{cls.__name__}.default_mapper()")
