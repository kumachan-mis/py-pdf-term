from os import path
from pathlib import Path
from xml.etree.ElementTree import Element, parse

from py_pdf_term.pdftoxml import PDFtoXMLConverter

from ..consts import FIXTURES_DIR


def test_convert_as_file(tmp_path: Path):
    converter = PDFtoXMLConverter()
    pdf_path = path.join(FIXTURES_DIR, "py-pdf-term.pdf")
    xml_path = path.join(tmp_path.as_posix(), "py-pdf-term.xml")

    converter.convert_as_file(pdf_path, xml_path)

    assert path.exists(xml_path)

    assert_xml_content(parse(xml_path).getroot())


def test_convert_as_element() -> None:
    converter = PDFtoXMLConverter()
    pdf_path = path.join(FIXTURES_DIR, "py-pdf-term.pdf")

    tree = converter.convert_as_element(pdf_path)

    assert_xml_content(tree.xml_root)


def assert_xml_content(root: Element):
    pages = list(root.iter("page"))

    assert len(pages) == 7

    assert pages[0].attrib["id"] == "1"
    assert len(list(pages[0])) == len(list(pages[0].iter("text")))
    assert pages[0].findtext("text") == "py-pdf-term"

    assert pages[1].attrib["id"] == "2"
    assert len(list(pages[1])) == len(list(pages[1].iter("text")))
    assert pages[1].findtext("text") == "Motivation"

    assert pages[2].attrib["id"] == "3"
    assert len(list(pages[2])) == len(list(pages[2].iter("text")))
    assert pages[2].findtext("text") == "Features - for laboratory use"

    assert pages[3].attrib["id"] == "4"
    assert len(list(pages[3])) == len(list(pages[3].iter("text")))
    assert pages[3].findtext("text") == "Features - for practical use"

    assert pages[4].attrib["id"] == "5"
    assert len(list(pages[4])) == len(list(pages[4].iter("text")))
    assert pages[4].findtext("text") == "5-layers architecture"

    assert pages[5].attrib["id"] == "6"
    assert len(list(pages[5])) == len(list(pages[5].iter("text")))
    assert pages[5].findtext("text") == "5-layers architecture"

    assert pages[6].attrib["id"] == "7"
    assert len(list(pages[6])) == len(list(pages[6].iter("text")))
    assert pages[6].findtext("text") == "5-layers architecture"
