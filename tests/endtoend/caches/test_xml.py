from pathlib import Path
from xml.etree import ElementTree

from py_pdf_term.configs import XMLLayerConfig
from py_pdf_term.endtoend.caches import XMLLayerFileCache, XMLLayerNoCache
from py_pdf_term.pdftoxml import PDFnXMLElement


def test_file_cache(tmp_path: Path) -> None:
    cache = XMLLayerFileCache(tmp_path.as_posix())

    pdf_path = "test.pdf"
    first_pdfnxml = PDFnXMLElement(pdf_path, ElementTree.Element("first"))
    second_pdfnxml = PDFnXMLElement(pdf_path, ElementTree.Element("second"))
    config = XMLLayerConfig()

    assert cache.load(pdf_path, config) is None

    cache.store(first_pdfnxml, config)
    assert cache.load(pdf_path, config) == first_pdfnxml

    cache.store(second_pdfnxml, config)
    assert cache.load(pdf_path, config) == second_pdfnxml

    cache.remove(pdf_path, config)
    assert cache.load(pdf_path, config) is None

    cache.remove(pdf_path, config)
    assert cache.load(pdf_path, config) is None


def test_file_cache_multiple(tmp_path: Path) -> None:
    cache = XMLLayerFileCache(tmp_path.as_posix())

    pdf_path1 = "test1.pdf"
    pdfnxml1 = PDFnXMLElement(pdf_path1, ElementTree.Element("test1"))
    pdf_path2 = "test2.pdf"
    pdfnxml2 = PDFnXMLElement(pdf_path2, ElementTree.Element("test2"))
    config = XMLLayerConfig()

    assert cache.load(pdf_path1, config) is None
    assert cache.load(pdf_path2, config) is None

    cache.store(pdfnxml1, config)
    assert cache.load(pdf_path1, config) == pdfnxml1
    assert cache.load(pdf_path2, config) is None

    cache.store(pdfnxml2, config)
    assert cache.load(pdf_path1, config) == pdfnxml1
    assert cache.load(pdf_path2, config) == pdfnxml2

    cache.remove(pdf_path1, config)
    assert cache.load(pdf_path1, config) is None
    assert cache.load(pdf_path2, config) == pdfnxml2

    cache.remove(pdf_path2, config)
    assert cache.load(pdf_path1, config) is None
    assert cache.load(pdf_path2, config) is None


def test_no_cache(tmp_path: Path) -> None:
    cache = XMLLayerNoCache(tmp_path.as_posix())

    pdf_path = "test.pdf"
    first_pdfnxml = PDFnXMLElement(pdf_path, ElementTree.Element("first"))
    second_pdfnxml = PDFnXMLElement(pdf_path, ElementTree.Element("second"))
    config = XMLLayerConfig()

    assert cache.load(pdf_path, config) is None

    cache.store(first_pdfnxml, config)
    assert cache.load(pdf_path, config) is None

    cache.store(second_pdfnxml, config)
    assert cache.load(pdf_path, config) is None

    cache.remove(pdf_path, config)
    assert cache.load(pdf_path, config) is None

    cache.remove(pdf_path, config)
    assert cache.load(pdf_path, config) is None
