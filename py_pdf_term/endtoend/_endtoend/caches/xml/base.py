from abc import ABCMeta, abstractmethod

from py_pdf_term.pdftoxml import PDFnXMLElement

from ...configs import XMLLayerConfig


class BaseXMLLayerCache(metaclass=ABCMeta):
    """Base class for XML layer caches. An XML layer cache is expected to store and
    load XML elements per a PDF file.

    Args
    ----
        cache_dir:
            Directory path to store cache files.
    """

    def __init__(self, cache_dir: str) -> None:
        pass

    @abstractmethod
    def load(self, pdf_path: str, config: XMLLayerConfig) -> PDFnXMLElement | None:
        """Load XML elements from a cache file.

        Args
        ----
            pdf_path:
                Path to a PDF file to load XML elements.
            config:
                Configuration for the XML layer. The configuration is used to
                determine the cache file path.

        Returns
        -------
            PDFnXMLElement | None:
                Loaded XML elements. If there is no cache file, this method returns
                None.
        """

        raise NotImplementedError(f"{self.__class__.__name__}.load()")

    @abstractmethod
    def store(self, pdfnxml: PDFnXMLElement, config: XMLLayerConfig) -> None:
        """Store XML elements to a cache file.

        Args
        ----
            pdfnxml:
                The XML elements to store.
            config:
                Configuration for the XML layer. The configuration is used to
                determine the cache file path.
        """

        raise NotImplementedError(f"{self.__class__.__name__}.store()")

    @abstractmethod
    def remove(self, pdf_path: str, config: XMLLayerConfig) -> None:
        """Remove a cache file.

        Args
        ----
            pdf_path:
                Path to a PDF file to remove a cache file.
            config:
                Configuration for the XML layer. The configuration is used to
                determine the cache file path.
        """

        raise NotImplementedError(f"{self.__class__.__name__}.remove()")
