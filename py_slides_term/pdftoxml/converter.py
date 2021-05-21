from io import BytesIO, BufferedReader
from typing import BinaryIO, Optional
from xml.etree.ElementTree import fromstring

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.layout import LAParams

from .textful import TextfulXMLConverter
from .data import PDFnXMLPath, PDFnXMLElement


class PDFtoXMLConverter:
    # public
    def convert_as_file(
        self,
        pdf_path: str,
        xml_path: str,
        nfc_norm: bool = True,
        include_parrern: Optional[str] = None,
        exclude_parrern: Optional[str] = None,
    ) -> PDFnXMLPath:
        with open(pdf_path, "rb") as pdf_file, open(xml_path, "wb") as xml_file:
            self._run(pdf_file, xml_file, nfc_norm, include_parrern, exclude_parrern)

        return PDFnXMLPath(pdf_path, xml_path)

    def convert_as_element(
        self,
        pdf_path: str,
        nfc_norm: bool = True,
        include_parrern: Optional[str] = None,
        exclude_parrern: Optional[str] = None,
    ) -> PDFnXMLElement:
        with open(pdf_path, "rb") as pdf_file, BytesIO() as xml_stream:
            self._run(pdf_file, xml_stream, nfc_norm, include_parrern, exclude_parrern)
            xml_element = fromstring(xml_stream.getvalue().decode("utf-8"))

        return PDFnXMLElement(pdf_path, xml_element)

    # private
    def _run(
        self,
        pdf_file: BufferedReader,
        xml_io: BinaryIO,
        nfc_norm: bool,
        include_parrern: Optional[str],
        exclude_parrern: Optional[str],
    ):
        manager = PDFResourceManager()
        laparams = LAParams(char_margin=2.0, line_margin=0.5, word_margin=0.2)
        converter = TextfulXMLConverter(
            manager,
            xml_io,
            laparams=laparams,
            nfc_norm=nfc_norm,
            include_pattern=include_parrern,
            exclude_parrern=exclude_parrern,
        )
        page_interpreter = PDFPageInterpreter(manager, converter)

        pages = PDFPage.get_pages(pdf_file)  # type: ignore
        converter.write_header()
        for page in pages:
            page_interpreter.process_page(page)  # type: ignore
        converter.write_footer()
