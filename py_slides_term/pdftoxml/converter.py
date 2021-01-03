from io import BytesIO

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

from .textful import TextfulXMLConverter
from .data import PDFnXMLPath, PDFnXMLContent


class PDFtoXMLConverter:
    # public
    def convert_as_file(self, pdf_path: str, xml_path: str) -> PDFnXMLPath:
        manager = PDFResourceManager()

        with open(pdf_path, "rb") as pdf_file, open(xml_path, "wb") as xml_file:
            converter = TextfulXMLConverter(manager, xml_file, stripcontrol=True)
            page_interpreter = PDFPageInterpreter(manager, converter)
            pages = PDFPage.get_pages(pdf_file)  # pyright:reportUnknownMemberType=false

            converter.write_header()
            for page in pages:
                page_interpreter.process_page(page)
            converter.write_footer()

        return PDFnXMLPath(pdf_path, xml_path)

    def convert_as_content(self, pdf_path: str) -> PDFnXMLContent:
        manager = PDFResourceManager()

        with open(pdf_path, "rb") as pdf_file, BytesIO() as xml_stream:
            converter = TextfulXMLConverter(manager, xml_stream, stripcontrol=True)
            page_interpreter = PDFPageInterpreter(manager, converter)
            pages = PDFPage.get_pages(pdf_file)  # pyright:reportUnknownMemberType=false

            converter.write_header()
            for page in pages:
                page_interpreter.process_page(page)
            converter.write_footer()

            xml_content = xml_stream.getvalue().decode("utf-8")

        return PDFnXMLContent(pdf_path, xml_content)
