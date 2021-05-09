from typing import Type

from ..base import BaseMapper
from ...caches import (
    BaseCandidateLayerCache,
    CandidateLayerNoCache,
    CandidateLayerFileCache,
)


class CandidateLayerCacheMapper(BaseMapper[Type[BaseCandidateLayerCache]]):
    @classmethod
    def default_mapper(cls):
        module_path = "py_slides_term.caches"
        default_mapper = cls()

        cache_clses = [
            CandidateLayerNoCache,
            CandidateLayerFileCache,
        ]
        for augmenter_cls in cache_clses:
            default_mapper.add(f"{module_path}.{augmenter_cls.__name__}", augmenter_cls)

        return default_mapper
