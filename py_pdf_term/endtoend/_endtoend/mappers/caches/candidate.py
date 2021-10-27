from typing import Type

from ...caches import (
    BaseCandidateLayerCache,
    CandidateLayerFileCache,
    CandidateLayerNoCache,
)
from ..base import BaseMapper
from ..consts import PACKAGE_NAME


class CandidateLayerCacheMapper(BaseMapper[Type[BaseCandidateLayerCache]]):
    @classmethod
    def default_mapper(cls) -> "CandidateLayerCacheMapper":
        default_mapper = cls()

        cache_clses = [CandidateLayerNoCache, CandidateLayerFileCache]
        for cache_cls in cache_clses:
            default_mapper.add(f"{PACKAGE_NAME}.{cache_cls.__name__}", cache_cls)

        return default_mapper
