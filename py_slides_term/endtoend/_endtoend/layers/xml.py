from typing import Optional

from ..caches import DEFAULT_CACHE_DIR
from ..configs import XMLLayerConfig
from ..mappers import XMLLayerCacheMapper
from py_slides_term.pdftoxml import PDFtoXMLConverter, PDFnXMLElement


class XMLLayer:
    def __init__(
        self,
        config: Optional[XMLLayerConfig] = None,
        cache_mapper: Optional[XMLLayerCacheMapper] = None,
        cache_dir: str = DEFAULT_CACHE_DIR,
    ) -> None:
        if config is None:
            config = XMLLayerConfig()
        if cache_mapper is None:
            cache_mapper = XMLLayerCacheMapper.default_mapper()

        cache_cls = cache_mapper.find(config.cache)

        self._converter = PDFtoXMLConverter()
        self._cache = cache_cls(cache_dir=cache_dir)
        self._config = config

    def create_pdfnxml(self, pdf_path: str) -> PDFnXMLElement:
        pdfnxml = None
        pdfnxml = self._cache.load(pdf_path, self._config)

        if pdfnxml is None:
            pdfnxml = self._converter.convert_as_element(
                pdf_path,
                nfc_norm=self._config.nfc_norm,
                include_parrern=self._config.include_pattern,
                exclude_parrern=self._config.exclude_pattern,
            )

        self._cache.store(pdfnxml, self._config)

        return pdfnxml

    def remove_cache(self, pdf_path: str) -> None:
        self._cache.remove(pdf_path, self._config)