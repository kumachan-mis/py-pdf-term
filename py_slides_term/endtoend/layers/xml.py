from typing import Optional

from ..caches import XMLLayerCache, DEFAULT_CACHE_DIR
from ..configs import XMLLayerConfig
from py_slides_term.pdftoxml import PDFtoXMLConverter, PDFnXMLContent


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

    def process(self, pdf_path: str) -> PDFnXMLContent:
        pdfnxml = None
        if self._config.use_cache:
            pdfnxml = self._cache.load(pdf_path, self._config)
        if pdfnxml is None:
            pdfnxml = self._converter.convert_as_content(pdf_path)
        if self._config.use_cache:
            self._cache.store(pdfnxml, self._config)

        return pdfnxml
