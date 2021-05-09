from typing import Type

from ..base import BaseMapper
from ...caches import BaseXMLLayerCache, XMLLayerNoCache, XMLLayerFileCache


class XMLLayerCacheMapper(BaseMapper[Type[BaseXMLLayerCache]]):
    @classmethod
    def default_mapper(cls):
        module_path = "py_slides_term.caches"
        default_mapper = cls()

        cache_clses = [XMLLayerNoCache, XMLLayerFileCache]
        for cache_cls in cache_clses:
            default_mapper.add(f"{module_path}.{cache_cls.__name__}", cache_cls)

        return default_mapper
