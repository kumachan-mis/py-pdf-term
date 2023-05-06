from xml.etree.ElementTree import parse

from py_pdf_term.candidates import CandidateTermExtractor
from py_pdf_term.pdftoxml import PDFnXMLElement, PDFnXMLPath

from ..fixtures import PyPDFTermFixture


def test_extract_from_domain_files() -> None:
    extractor = CandidateTermExtractor()

    domain_candidates = extractor.extract_from_domain_files(
        "test", [PDFnXMLPath(PyPDFTermFixture.PDF_PATH, PyPDFTermFixture.XML_PATH)]
    )

    assert domain_candidates.domain == "test"
    assert len(domain_candidates.pdfs) == 1
    PyPDFTermFixture.assert_pdf_candidates(domain_candidates.pdfs[0])


def test_extract_from_xml_file() -> None:
    extractor = CandidateTermExtractor()

    pdf_candidates = extractor.extract_from_xml_file(
        PDFnXMLPath(PyPDFTermFixture.PDF_PATH, PyPDFTermFixture.XML_PATH)
    )

    PyPDFTermFixture.assert_pdf_candidates(pdf_candidates)


def test_extract_from_domain_elements() -> None:
    extractor = CandidateTermExtractor()

    xml_root = parse(PyPDFTermFixture.XML_PATH).getroot()

    domain_candidates = extractor.extract_from_domain_elements(
        "test", [PDFnXMLElement(PyPDFTermFixture.PDF_PATH, xml_root)]
    )

    assert domain_candidates.domain == "test"
    assert len(domain_candidates.pdfs) == 1
    PyPDFTermFixture.assert_pdf_candidates(domain_candidates.pdfs[0])


def test_extract_from_xml_element() -> None:
    extractor = CandidateTermExtractor()

    xml_root = parse(PyPDFTermFixture.XML_PATH).getroot()

    pdf_candidates = extractor.extract_from_xml_element(
        PDFnXMLElement(PyPDFTermFixture.PDF_PATH, xml_root)
    )

    PyPDFTermFixture.assert_pdf_candidates(pdf_candidates)
