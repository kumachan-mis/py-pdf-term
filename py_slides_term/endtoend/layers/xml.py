from typing import Optional

from ..caches import XMLLayerCache, DEFAULT_CACHE_DIR
from ..configs import XMLLayerConfig
from py_slides_term.pdftoxml import PDFtoXMLConverter, PDFnXMLElement


class XMLLayer:
    # public
    def __init__(
        self,
        config: Optional[XMLLayerConfig] = None,
        cache_dir: str = DEFAULT_CACHE_DIR,
    ):
        if config is None:
            config = XMLLayerConfig()

        self._converter = PDFtoXMLConverter()
        self._cache = XMLLayerCache(cache_dir=cache_dir)
        self._config = config

    def create_pdfnxml(self, pdf_path: str) -> PDFnXMLElement:
        if self._config.use_cache:
            pdfnxml = self._cache.load(pdf_path, self._config)
            if pdfnxml is not None:
                return pdfnxml

        pdfnxml = self._converter.convert_as_content(pdf_path)

        if self._config.use_cache:
            self._cache.store(pdfnxml, self._config)

        return pdfnxml

    def remove_cache(self, pdf_path: str):
        self._cache.remove(pdf_path, self._config)
