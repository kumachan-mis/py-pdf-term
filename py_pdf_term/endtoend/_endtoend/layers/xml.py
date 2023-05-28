from py_pdf_term.pdftoxml import PDFnXMLElement, PDFtoXMLConverter

from ..caches import DEFAULT_CACHE_DIR
from ..configs import XMLLayerConfig
from ..mappers import BinaryOpenerMapper, XMLLayerCacheMapper


class XMLLayer:
    """Layer to create textful XML elements from a PDF file.

    Args
    ----
        config:
            Configuration for this layer. If None, the default configuration is used.
        bin_opener_mapper:
            Mapper to find binary opener classes from configuration. If None, the
            default mapper is used.
        cache_mapper:
            Mapper to find cache class from configuration. If None, the default mapper
            is used.
        cache_dir:
            Directory path to store cache files. If None, the default directory is
            used.
    """

    def __init__(
        self,
        config: XMLLayerConfig | None = None,
        bin_opener_mapper: BinaryOpenerMapper | None = None,
        cache_mapper: XMLLayerCacheMapper | None = None,
        cache_dir: str = DEFAULT_CACHE_DIR,
    ) -> None:
        if config is None:
            config = XMLLayerConfig()
        if bin_opener_mapper is None:
            bin_opener_mapper = BinaryOpenerMapper.default_mapper()
        if cache_mapper is None:
            cache_mapper = XMLLayerCacheMapper.default_mapper()

        bin_opener_cls = bin_opener_mapper.find(config.bin_opener)
        cache_cls = cache_mapper.find(config.cache)

        bin_opener = bin_opener_cls()
        self._converter = PDFtoXMLConverter(bin_opener=bin_opener)
        self._cache = cache_cls(cache_dir=cache_dir)
        self._config = config

    def create_pdfnxml(self, pdf_path: str) -> PDFnXMLElement:
        """Create a PDFnXMLElement from a PDF file.

        Args
        ----
            pdf_path:
                Path to a PDF file.

        Returns
        -------
            PDFnXMLElement created from the PDF file.
        """

        pdfnxml = None
        pdfnxml = self._cache.load(pdf_path, self._config)

        if pdfnxml is None:
            pdfnxml = self._converter.convert_as_element(
                pdf_path,
                nfc_norm=self._config.nfc_norm,
                include_pattern=self._config.include_pattern,
                exclude_pattern=self._config.exclude_pattern,
            )

        self._cache.store(pdfnxml, self._config)

        return pdfnxml

    def remove_cache(self, pdf_path: str) -> None:
        """Remove a cache file for a PDF file.

        Args
        ----
            pdf_path:
                Path to a PDF file.
        """

        self._cache.remove(pdf_path, self._config)
