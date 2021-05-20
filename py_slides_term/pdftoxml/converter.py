from io import BytesIO
from typing import Optional
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
    ) -> PDFnXMLPath:
        manager = PDFResourceManager()
        params = LAParams()

        with open(pdf_path, "rb") as pdf_file, open(xml_path, "wb") as xml_file:
            converter = TextfulXMLConverter(
                manager,
                xml_file,
                laparams=params,
                nfc_norm=nfc_norm,
                include_pattern=include_parrern,
            )
            page_interpreter = PDFPageInterpreter(manager, converter)
            pages = PDFPage.get_pages(pdf_file)  # type: ignore

            converter.write_header()
            for page in pages:
                page_interpreter.process_page(page)  # type: ignore
            converter.write_footer()

        return PDFnXMLPath(pdf_path, xml_path)

    def convert_as_element(
        self,
        pdf_path: str,
        nfc_norm: bool = True,
        include_parrern: Optional[str] = None,
    ) -> PDFnXMLElement:
        manager = PDFResourceManager()
        params = LAParams()

        with open(pdf_path, "rb") as pdf_file, BytesIO() as xml_stream:
            converter = TextfulXMLConverter(
                manager,
                xml_stream,
                laparams=params,
                nfc_norm=nfc_norm,
                include_pattern=include_parrern,
            )
            page_interpreter = PDFPageInterpreter(manager, converter)
            pages = PDFPage.get_pages(pdf_file)  # type: ignore

            converter.write_header()
            for page in pages:
                page_interpreter.process_page(page)  # type: ignore
            converter.write_footer()

            xml_element = fromstring(xml_stream.getvalue().decode("utf-8"))

        return PDFnXMLElement(pdf_path, xml_element)
