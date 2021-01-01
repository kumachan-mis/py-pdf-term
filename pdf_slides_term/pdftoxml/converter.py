from io import BufferedReader, BufferedWriter, BytesIO
from typing import Union

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

from .textful import TextfulXMLConverter


class PDFtoXMLConverter:
    # public
    def convert_between_path(self, pdf_path: str, xml_path: str) -> None:
        manager = PDFResourceManager()

        with open(pdf_path, "rb") as pdf_file, open(xml_path, "wb") as xml_file:
            converter = TextfulXMLConverter(manager, xml_file, stripcontrol=True)
            page_interpreter = PDFPageInterpreter(manager, converter)
            pages = PDFPage.get_pages(pdf_file)  # pyright:reportUnknownMemberType=false

            converter.write_header()
            for page in pages:
                page_interpreter.process_page(page)
            converter.write_footer()

    def convert_between_stream(
        self, pdf_stream: BufferedReader, xml_stream: Union[BufferedWriter, BytesIO]
    ) -> None:
        manager = PDFResourceManager()

        converter = TextfulXMLConverter(manager, xml_stream, stripcontrol=True)
        page_interpreter = PDFPageInterpreter(manager, converter)
        pages = PDFPage.get_pages(pdf_stream)  # pyright:reportUnknownMemberType=false

        converter.write_header()
        for page in pages:
            page_interpreter.process_page(page)
        converter.write_footer()
