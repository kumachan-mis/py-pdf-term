from typing import Any, Type

from ...caches import (
    BaseMethodLayerDataCache,
    BaseMethodLayerRankingCache,
    MethodLayerDataFileCache,
    MethodLayerDataNoCache,
    MethodLayerRankingFileCache,
    MethodLayerRankingNoCache,
)
from ..base import BaseMapper
from ..consts import PACKAGE_NAME


class MethodLayerRankingCacheMapper(BaseMapper[Type[BaseMethodLayerRankingCache]]):
    @classmethod
    def default_mapper(cls) -> "MethodLayerRankingCacheMapper":
        default_mapper = cls()

        cache_clses = [MethodLayerRankingNoCache, MethodLayerRankingFileCache]
        for cache_cls in cache_clses:
            default_mapper.add(f"{PACKAGE_NAME}.{cache_cls.__name__}", cache_cls)

        return default_mapper


class MethodLayerDataCacheMapper(BaseMapper[Type[BaseMethodLayerDataCache[Any]]]):
    @classmethod
    def default_mapper(cls) -> "MethodLayerDataCacheMapper":
        default_mapper = cls()

        cache_clses = [
            ("MethodLayerDataNoCache", MethodLayerDataNoCache[Any]),
            ("MethodLayerDataFileCache", MethodLayerDataFileCache[Any]),
        ]
        for name, cache_cls in cache_clses:
            default_mapper.add(f"{PACKAGE_NAME}.{name}", cache_cls)

        return default_mapper
