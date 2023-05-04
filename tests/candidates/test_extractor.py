from os import path
from typing import List, Union
from xml.etree.ElementTree import parse

from py_pdf_term.candidates import CandidateTermExtractor, PDFCandidateTermList
from py_pdf_term.pdftoxml import PDFnXMLElement, PDFnXMLPath
from py_pdf_term.tokenizers import Term

FIXTURES_DIR = path.join(path.dirname(__file__), "..", "..", "test-fixtures")


def test_extract_from_domain_files() -> None:
    extractor = CandidateTermExtractor()

    pdf_path = path.join(FIXTURES_DIR, "py-pdf-term.pdf")
    xml_path = path.join(FIXTURES_DIR, "py-pdf-term.xml")

    domain_candidates = extractor.extract_from_domain_files(
        "test", [PDFnXMLPath(pdf_path, xml_path)]
    )

    assert domain_candidates.domain == "test"
    assert len(domain_candidates.pdfs) == 1

    assert_pdf_candidtes(domain_candidates.pdfs[0])


def test_extract_from_xml_file() -> None:
    extractor = CandidateTermExtractor()

    pdf_path = path.join(FIXTURES_DIR, "py-pdf-term.pdf")
    xml_path = path.join(FIXTURES_DIR, "py-pdf-term.xml")

    pdf_candidates = extractor.extract_from_xml_file(PDFnXMLPath(pdf_path, xml_path))

    assert_pdf_candidtes(pdf_candidates)


def test_extract_from_domain_elements() -> None:
    extractor = CandidateTermExtractor()

    pdf_path = path.join(FIXTURES_DIR, "py-pdf-term.pdf")
    xml_path = path.join(FIXTURES_DIR, "py-pdf-term.xml")
    xml_root = parse(xml_path).getroot()

    domain_candidates = extractor.extract_from_domain_elements(
        "test", [PDFnXMLElement(pdf_path, xml_root)]
    )

    assert domain_candidates.domain == "test"
    assert len(domain_candidates.pdfs) == 1

    assert_pdf_candidtes(domain_candidates.pdfs[0])


def test_extract_from_xml_element() -> None:
    extractor = CandidateTermExtractor()

    pdf_path = path.join(FIXTURES_DIR, "py-pdf-term.pdf")
    xml_path = path.join(FIXTURES_DIR, "py-pdf-term.xml")
    xml_root = parse(xml_path).getroot()

    pdf_candidates = extractor.extract_from_xml_element(
        PDFnXMLElement(pdf_path, xml_root)
    )

    assert_pdf_candidtes(pdf_candidates)


def assert_pdf_candidtes(pdf_candidates: PDFCandidateTermList) -> None:
    def find_candidate_by_text(text: str, candidates: List[Term]) -> Union[Term, None]:
        return next(filter(lambda t: str(t) == text, candidates), None)

    assert pdf_candidates.pdf_path == path.join(FIXTURES_DIR, "py-pdf-term.pdf")
    assert len(pdf_candidates.pages) == 7

    candidates = pdf_candidates.pages[0]
    assert candidates.page_num == 1

    term = find_candidate_by_text("py-pdf-term", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 52.000) < 0.001
    assert term.ncolor == "(0.0, 0.0, 0.0)"

    term = find_candidate_by_text("Python", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 21.700) < 0.001
    assert term.ncolor == "(0.34901962, 0.34901962, 0.34901962)"

    candidates = pdf_candidates.pages[1]
    assert candidates.page_num == 2

    term = find_candidate_by_text("Motivation", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 25.200) < 0.001
    assert term.ncolor == "(0.0, 0.0, 0.0)"

    term = find_candidate_by_text("practical use", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 20.000) < 0.001
    assert term.ncolor == "(1.0, 0.0, 0.0)"

    candidates = pdf_candidates.pages[2]
    assert candidates.page_num == 3

    term = find_candidate_by_text("laboratory use", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 25.200) < 0.001
    assert term.ncolor == "(0.0, 0.0, 0.0)"

    term = find_candidate_by_text("ranking algorithms", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 20.000) < 0.001
    assert term.ncolor == "(0.34901962, 0.34901962, 0.34901962)"

    candidates = pdf_candidates.pages[3]
    assert candidates.page_num == 4

    term = find_candidate_by_text("practical use", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 25.200) < 0.001
    assert term.ncolor == "(0.0, 0.0, 0.0)"

    term = find_candidate_by_text("cache mechanism", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 20.000) < 0.001
    assert term.ncolor == "(0.34901962, 0.34901962, 0.34901962)"

    candidates = pdf_candidates.pages[4]
    assert candidates.page_num == 5

    term = find_candidate_by_text("XML Layer", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 0.0) < 0.001
    assert term.ncolor == "(0.0, 0.0, 0.0)"

    term = find_candidate_by_text("Candidate Term Layer", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 0.0) < 0.001
    assert term.ncolor == "(0.0, 0.0, 0.0)"

    candidates = pdf_candidates.pages[5]
    assert candidates.page_num == 6

    term = find_candidate_by_text("Method Layer", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 0.0) < 0.001
    assert term.ncolor == "(0.0, 0.0, 0.0)"

    term = find_candidate_by_text("Styling Layer", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 0.0) < 0.001
    assert term.ncolor == "(0.0, 0.0, 0.0)"

    candidates = pdf_candidates.pages[6]
    assert candidates.page_num == 7

    term = find_candidate_by_text("Technical Term Layer", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 0.0) < 0.001
    assert term.ncolor == "(0.0, 0.0, 0.0)"
