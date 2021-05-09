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

        cache_clses = [
            MethodLayerRankingNoCache,
            MethodLayerRankingFileCache,
        ]
        for augmenter_cls in cache_clses:
            default_mapper.add(f"{module_path}.{augmenter_cls.__name__}", augmenter_cls)

        return default_mapper


class MethodLayerDataCacheMapper(BaseMapper[Type[BaseMethodLayerDataCache[Any]]]):
    @classmethod
    def default_mapper(cls):
        module_path = "py_slides_term.caches"
        default_mapper = cls()

        cache_clses = [
            MethodLayerDataNoCache[Any],
            MethodLayerDataFileCache[Any],
        ]
        for augmenter_cls in cache_clses:
            default_mapper.add(f"{module_path}.{augmenter_cls.__name__}", augmenter_cls)

        return default_mapper
