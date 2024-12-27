from io import BytesIO
from typing import BinaryIO
from xml.etree.ElementTree import fromstring

from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage

from .binopeners import BaseBinaryOpener, StandardBinaryOpener
from .data import PDFnXMLElement, PDFnXMLPath
from .textful import TextfulXMLConverter


class PDFtoXMLConverter:
    """Converter from PDF to textful XML format.

    Args
    ----
        bin_opener:
            Binary opener to open PDF and XML files. If None, StandardBinaryOpener is
            used, which opens files with the standard open function in Python.
    """

    def __init__(self, bin_opener: BaseBinaryOpener | None = None) -> None:
        if bin_opener is None:
            bin_opener = StandardBinaryOpener()

        self._bin_opener = bin_opener

    def convert_as_file(
        self,
        pdf_path: str,
        xml_path: str,
        nfc_norm: bool = True,
        include_pattern: str | None = None,
        exclude_pattern: str | None = None,
    ) -> PDFnXMLPath:
        """Convert a PDF file to a textful XML file.

        Args
        ----
            pdf_path:
                Path to a PDF file.
            xml_path:
                Path to a XML file to output.
            nfc_norm:
                If True, normalize text to NFC, otherwise keep original.
            include_pattern:
                Regular expression pattern of text to include in the output.
            exclude_pattern:
                Regular expression pattern of text to exclude from the output
                (overrides include_pattern).

        Returns
        -------
            Pair of path to the PDF file and that to the output XML file.
        """

        pdf_io = self._bin_opener.open(pdf_path, "rb")
        xml_io = self._bin_opener.open(xml_path, "wb")
        self._run(pdf_io, xml_io, nfc_norm, include_pattern, exclude_pattern)
        xml_io.close()
        pdf_io.close()
        return PDFnXMLPath(pdf_path, xml_path)

    def convert_as_element(
        self,
        pdf_path: str,
        nfc_norm: bool = True,
        include_pattern: str | None = None,
        exclude_pattern: str | None = None,
    ) -> PDFnXMLElement:
        """Convert a PDF file to a textful XML element.

        Args
        ----
            pdf_path:
                Path to a PDF file.
            nfc_norm:
                If True, normalize text to NFC, otherwise keep original.
            include_pattern:
                Regular expression pattern of text to include in the output.
            exclude_pattern:
                Regular expression pattern of text to exclude from the output
                (overrides include_pattern).

        Returns
        -------
            Pair of path to the PDF file and XML element tree of the output.
        """

        pdf_io = self._bin_opener.open(pdf_path, "rb")
        xml_io = BytesIO()
        self._run(pdf_io, xml_io, nfc_norm, include_pattern, exclude_pattern)
        xml_element = fromstring(xml_io.getvalue().decode("utf-8"))
        xml_io.close()
        pdf_io.close()
        return PDFnXMLElement(pdf_path, xml_element)

    def _run(
        self,
        pdf_io: BinaryIO,
        xml_io: BinaryIO,
        nfc_norm: bool,
        include_pattern: str | None,
        exclude_pattern: str | None,
    ) -> None:
        manager = PDFResourceManager()
        laparams = LAParams(char_margin=2.0, line_margin=0.5, word_margin=0.2)
        converter = TextfulXMLConverter(
            manager,
            xml_io,
            laparams=laparams,
            nfc_norm=nfc_norm,
            include_pattern=include_pattern,
            exclude_pattern=exclude_pattern,
        )
        page_interpreter = PDFPageInterpreter(manager, converter)

        pages = PDFPage.get_pages(pdf_io)
        converter.write_header()
        for page in pages:
            page_interpreter.process_page(page)
        converter.write_footer()
