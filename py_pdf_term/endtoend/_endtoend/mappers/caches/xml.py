from typing import Self

from py_pdf_term._common.consts import PACKAGE_NAME

from ...caches import BaseXMLLayerCache, XMLLayerFileCache, XMLLayerNoCache
from ..base import BaseMapper


class XMLLayerCacheMapper(BaseMapper[type[BaseXMLLayerCache]]):
    """Mapper to find XML layer cache classes."""

    @classmethod
    def default_mapper(cls) -> Self:
        default_mapper = cls()

        cache_clses: list[type[BaseXMLLayerCache]] = [
            XMLLayerNoCache,
            XMLLayerFileCache,
        ]
        for cache_cls in cache_clses:
            default_mapper.add(f"{PACKAGE_NAME}.{cache_cls.__name__}", cache_cls)

        return default_mapper
