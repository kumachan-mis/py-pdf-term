from typing import Type

from ..base import BaseMapper
from ..consts import PACKAGE_NAME
from ...caches import BaseStylingLayerCache, StylingLayerNoCache, StylingLayerFileCache


class StylingLayerCacheMapper(BaseMapper[Type[BaseStylingLayerCache]]):
    @classmethod
    def default_mapper(cls) -> "StylingLayerCacheMapper":
        default_mapper = cls()

        cache_clses = [StylingLayerNoCache, StylingLayerFileCache]
        for cache_cls in cache_clses:
            default_mapper.add(f"{PACKAGE_NAME}.{cache_cls.__name__}", cache_cls)

        return default_mapper