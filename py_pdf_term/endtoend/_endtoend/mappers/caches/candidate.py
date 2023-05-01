from typing import Type

from py_pdf_term._common.consts import PACKAGE_NAME

from ...caches import (
    BaseCandidateLayerCache,
    CandidateLayerFileCache,
    CandidateLayerNoCache,
)
from ..base import BaseMapper


class CandidateLayerCacheMapper(BaseMapper[Type[BaseCandidateLayerCache]]):
    """A mapper to find candidate layer cache classes."""

    @classmethod
    def default_mapper(cls) -> "CandidateLayerCacheMapper":
        default_mapper = cls()

        cache_clses = [CandidateLayerNoCache, CandidateLayerFileCache]
        for cache_cls in cache_clses:
            default_mapper.add(f"{PACKAGE_NAME}.{cache_cls.__name__}", cache_cls)

        return default_mapper
