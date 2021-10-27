from io import BytesIO
from typing import BinaryIO, Callable, Optional
from xml.etree.ElementTree import fromstring

from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFPageInterpreter, PDFResourceManager
from pdfminer.pdfpage import PDFPage

from .data import PDFnXMLElement, PDFnXMLPath
from .textful import TextfulXMLConverter


class PDFtoXMLConverter:
    def __init__(self, open_bin: Callable[[str, str], BinaryIO] = open):  # type: ignore
        self.open_bin = open_bin

    def convert_as_file(
        self,
        pdf_path: str,
        xml_path: str,
        nfc_norm: bool = True,
        include_pattern: Optional[str] = None,
        exclude_pattern: Optional[str] = None,
    ) -> PDFnXMLPath:
        pdf_io, xml_io = self.open_bin(pdf_path, "rb"), self.open_bin(xml_path, "wb")
        self._run(pdf_io, xml_io, nfc_norm, include_pattern, exclude_pattern)
        pdf_io.close(), xml_io.close()

        return PDFnXMLPath(pdf_path, xml_path)

    def convert_as_element(
        self,
        pdf_path: str,
        nfc_norm: bool = True,
        include_pattern: Optional[str] = None,
        exclude_pattern: Optional[str] = None,
    ) -> PDFnXMLElement:
        pdf_io, xml_io = self.open_bin(pdf_path, "rb"), BytesIO()
        self._run(pdf_io, xml_io, nfc_norm, include_pattern, exclude_pattern)
        xml_element = fromstring(xml_io.getvalue().decode("utf-8"))
        pdf_io.close(), xml_io.close()
        return PDFnXMLElement(pdf_path, xml_element)

    def _run(
        self,
        pdf_io: BinaryIO,
        xml_io: BinaryIO,
        nfc_norm: bool,
        include_pattern: Optional[str],
        exclude_pattern: Optional[str],
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

        pages = PDFPage.get_pages(pdf_io)  # type: ignore
        converter.write_header()
        for page in pages:
            page_interpreter.process_page(page)  # type: ignore
        converter.write_footer()
