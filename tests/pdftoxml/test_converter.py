from os import path
from pathlib import Path
from xml.etree.ElementTree import parse

from py_pdf_term.pdftoxml import PDFnXMLElement, PDFtoXMLConverter

from ..fixtures import PyPDFTermFixture


def test_convert_as_file(tmp_path: Path):
    converter = PDFtoXMLConverter()
    xml_path = path.join(tmp_path.as_posix(), PyPDFTermFixture.XML_NAME)

    converter.convert_as_file(PyPDFTermFixture.PDF_PATH, xml_path)
    pdfnxml = PDFnXMLElement(PyPDFTermFixture.PDF_PATH, parse(xml_path).getroot())

    assert path.exists(xml_path)
    PyPDFTermFixture.assert_pdfnxml(pdfnxml)


def test_convert_as_element() -> None:
    converter = PDFtoXMLConverter()

    pdfnxml = converter.convert_as_element(PyPDFTermFixture.PDF_PATH)

    PyPDFTermFixture.assert_pdfnxml(pdfnxml)
