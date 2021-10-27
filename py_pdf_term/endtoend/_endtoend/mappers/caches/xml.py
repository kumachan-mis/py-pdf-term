from typing import Type

from ...caches import BaseXMLLayerCache, XMLLayerFileCache, XMLLayerNoCache
from ..base import BaseMapper
from ..consts import PACKAGE_NAME


class XMLLayerCacheMapper(BaseMapper[Type[BaseXMLLayerCache]]):
    @classmethod
    def default_mapper(cls) -> "XMLLayerCacheMapper":
        default_mapper = cls()

        cache_clses = [XMLLayerNoCache, XMLLayerFileCache]
        for cache_cls in cache_clses:
            default_mapper.add(f"{PACKAGE_NAME}.{cache_cls.__name__}", cache_cls)

        return default_mapper
