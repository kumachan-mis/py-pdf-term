from typing import Any, Self

from py_pdf_term._common.consts import PACKAGE_NAME

from ...caches import (
    BaseMethodLayerDataCache,
    BaseMethodLayerRankingCache,
    MethodLayerDataFileCache,
    MethodLayerDataNoCache,
    MethodLayerRankingFileCache,
    MethodLayerRankingNoCache,
)
from ..base import BaseMapper


class MethodLayerRankingCacheMapper(BaseMapper[type[BaseMethodLayerRankingCache]]):
    """Mapper to find method layer ranking cache classes."""

    @classmethod
    def default_mapper(cls) -> Self:
        default_mapper = cls()

        cache_clses: list[type[BaseMethodLayerRankingCache]] = [
            MethodLayerRankingNoCache,
            MethodLayerRankingFileCache,
        ]
        for cache_cls in cache_clses:
            default_mapper.add(f"{PACKAGE_NAME}.{cache_cls.__name__}", cache_cls)

        return default_mapper


class MethodLayerDataCacheMapper(BaseMapper[type[BaseMethodLayerDataCache[Any]]]):
    """Mapper to find method layer data cache classes."""

    @classmethod
    def default_mapper(cls) -> Self:
        default_mapper = cls()

        cache_clses: list[tuple[str, type[BaseMethodLayerDataCache[Any]]]] = [
            ("MethodLayerDataNoCache", MethodLayerDataNoCache[Any]),
            ("MethodLayerDataFileCache", MethodLayerDataFileCache[Any]),
        ]
        for name, cache_cls in cache_clses:
            default_mapper.add(f"{PACKAGE_NAME}.{name}", cache_cls)

        return default_mapper
