from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

from .textful import TextfulXMLConverter


class PDFtoXMLConverter:
    # public
    def pdf_to_xml(self, pdf_path: str, xml_path: str) -> None:
        manager = PDFResourceManager()

        with open(pdf_path, "rb") as pdf_file, open(xml_path, "wb") as xml_file:
            converter = TextfulXMLConverter(manager, xml_file, stripcontrol=True)
            page_interpreter = PDFPageInterpreter(manager, converter)
            pages = PDFPage.get_pages(pdf_file)  # pyright:reportUnknownMemberType=false

            for page in pages:
                page_interpreter.process_page(page)

            converter.close()
