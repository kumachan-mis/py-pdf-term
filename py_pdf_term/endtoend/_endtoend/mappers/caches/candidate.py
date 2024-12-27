from typing import Self

from py_pdf_term._common.consts import PACKAGE_NAME

from ...caches import (
    BaseCandidateLayerCache,
    CandidateLayerFileCache,
    CandidateLayerNoCache,
)
from ..base import BaseMapper


class CandidateLayerCacheMapper(BaseMapper[type[BaseCandidateLayerCache]]):
    """Mapper to find candidate layer cache classes."""

    @classmethod
    def default_mapper(cls) -> Self:
        default_mapper = cls()

        cache_clses: list[type[BaseCandidateLayerCache]] = [
            CandidateLayerNoCache,
            CandidateLayerFileCache,
        ]
        for cache_cls in cache_clses:
            default_mapper.add(f"{PACKAGE_NAME}.{cache_cls.__name__}", cache_cls)

        return default_mapper
