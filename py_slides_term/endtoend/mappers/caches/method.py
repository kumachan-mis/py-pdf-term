from typing import Any, Type

from ..base import BaseMapper
from ...caches import (
    BaseMethodLayerRankingCache,
    MethodLayerRankingNoCache,
    MethodLayerRankingFileCache,
    BaseMethodLayerDataCache,
    MethodLayerDataNoCache,
    MethodLayerDataFileCache,
)


class MethodLayerRankingCacheMapper(BaseMapper[Type[BaseMethodLayerRankingCache]]):
    @classmethod
    def default_mapper(cls):
        module_path = "py_slides_term.caches"
        default_mapper = cls()

        cache_clses = [MethodLayerRankingNoCache, MethodLayerRankingFileCache]
        for cache_cls in cache_clses:
            default_mapper.add(f"{module_path}.{cache_cls.__name__}", cache_cls)

        return default_mapper


class MethodLayerDataCacheMapper(BaseMapper[Type[BaseMethodLayerDataCache[Any]]]):
    @classmethod
    def default_mapper(cls):
        module_path = "py_slides_term.caches"
        default_mapper = cls()

        cache_clses = [
            ("MethodLayerDataNoCache", MethodLayerDataNoCache[Any]),
            ("MethodLayerDataFileCache", MethodLayerDataFileCache[Any]),
        ]
        for name, cache_cls in cache_clses:
            default_mapper.add(f"{module_path}.{name}", cache_cls)

        return default_mapper
