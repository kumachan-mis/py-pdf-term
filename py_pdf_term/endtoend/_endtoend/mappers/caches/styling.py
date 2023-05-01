from typing import Type

from py_pdf_term._common.consts import PACKAGE_NAME

from ...caches import BaseStylingLayerCache, StylingLayerFileCache, StylingLayerNoCache
from ..base import BaseMapper


class StylingLayerCacheMapper(BaseMapper[Type[BaseStylingLayerCache]]):
    """A mapper to find styling layer cache classes."""

    @classmethod
    def default_mapper(cls) -> "StylingLayerCacheMapper":
        default_mapper = cls()

        cache_clses = [StylingLayerNoCache, StylingLayerFileCache]
        for cache_cls in cache_clses:
            default_mapper.add(f"{PACKAGE_NAME}.{cache_cls.__name__}", cache_cls)

        return default_mapper
