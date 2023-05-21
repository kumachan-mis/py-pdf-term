from os import path
from typing import List, Optional

from py_pdf_term import PDFTechnicalTermList
from py_pdf_term.candidates import PDFCandidateTermList
from py_pdf_term.methods import MethodTermRanking
from py_pdf_term.pdftoxml import PDFnXMLElement
from py_pdf_term.stylings import PDFStylingScoreList
from py_pdf_term.tokenizers import Term
from py_pdf_term._common.data import ScoredTerm

FIXTURES_DIR = path.abspath(path.join(path.dirname(__file__), "..", "test-fixtures"))


class PyPDFTermFixture:
    PDF_NAME = "py-pdf-term.pdf"
    XML_NAME = "py-pdf-term.xml"
    CANDIDATE_NAME = "py-pdf-term-candidate.json"
    METHOD_NAME = "py-pdf-term-method.json"
    STYLING_NAME = "py-pdf-term-styling.json"

    PDF_PATH = path.join(FIXTURES_DIR, PDF_NAME)
    XML_PATH = path.join(FIXTURES_DIR, XML_NAME)
    CANDIDATE_PATH = path.join(FIXTURES_DIR, CANDIDATE_NAME)
    METHOD_PATH = path.join(FIXTURES_DIR, METHOD_NAME)
    STYLING_PATH = path.join(FIXTURES_DIR, STYLING_NAME)

    @classmethod
    def assert_pdfnxml(cls, pdfnxml: PDFnXMLElement) -> None:
        assert pdfnxml.pdf_path == cls.PDF_PATH

        pages = list(pdfnxml.xml_root.iter("page"))

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

    @classmethod
    def assert_pdf_candidates(cls, pdf_candidates: PDFCandidateTermList) -> None:
        def find_candidate_by_text(text: str, candidates: List[Term]) -> Optional[Term]:
            return next(filter(lambda t: str(t) == text, candidates), None)

        assert pdf_candidates.pdf_path == cls.PDF_PATH
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

    @classmethod
    def assert_method_term_ranking(
        cls, ranking: MethodTermRanking, acceptance_rate: float = 0.7
    ) -> None:
        assert len(ranking.ranking) > 0
        assert all(
            map(
                lambda i: ranking.ranking[i].score >= ranking.ranking[i + 1].score,
                range(0, len(ranking.ranking) - 1),
            )
        )
        high_scored_terms = set(
            map(
                lambda t: t.term,
                ranking.ranking[: int(len(ranking.ranking) * acceptance_rate)],
            )
        )
        assert "5-layer architecture" in high_scored_terms
        assert "xml layer" in high_scored_terms
        assert "candidate term layer" in high_scored_terms
        assert "method layer" in high_scored_terms
        assert "styling layer" in high_scored_terms
        assert "technical term layer" in high_scored_terms

    @classmethod
    def assert_pdf_stylings(
        cls, pdf_stylings: PDFStylingScoreList, acceptance_rate: float = 0.7
    ) -> None:
        def ranking_is_ordered(ranking: List[ScoredTerm]) -> bool:
            return all(
                map(
                    lambda i: ranking[i].score >= ranking[i + 1].score,
                    range(0, len(ranking) - 1),
                )
            )

        def get_high_scored_terms(ranking: List[ScoredTerm]) -> set[str]:
            return set(
                map(
                    lambda t: t.term,
                    ranking[: int(len(ranking) * acceptance_rate)],
                )
            )

        assert pdf_stylings.pdf_path == cls.PDF_PATH
        assert len(pdf_stylings.pages) == 7

        ranking = pdf_stylings.pages[0].ranking
        assert ranking_is_ordered(ranking)
        high_scored_terms = get_high_scored_terms(ranking)
        assert "py-pdf-term" in high_scored_terms

        ranking = pdf_stylings.pages[1].ranking
        assert ranking_is_ordered(ranking)
        high_scored_terms = get_high_scored_terms(ranking)
        assert "motivation" in high_scored_terms
        assert "laboratory use" in high_scored_terms
        assert "practical use" in high_scored_terms

        ranking = pdf_stylings.pages[2].ranking
        assert ranking_is_ordered(ranking)
        high_scored_terms = get_high_scored_terms(ranking)
        assert "feature" in high_scored_terms
        assert "laboratory use" in high_scored_terms

        ranking = pdf_stylings.pages[3].ranking
        assert ranking_is_ordered(ranking)
        high_scored_terms = get_high_scored_terms(ranking)
        assert "feature" in high_scored_terms
        assert "practical use" in high_scored_terms

        ranking = pdf_stylings.pages[4].ranking
        assert ranking_is_ordered(ranking)
        high_scored_terms = get_high_scored_terms(ranking)
        assert "5-layer architecture" in high_scored_terms
        assert "xml layer" in high_scored_terms
        assert "candidate term layer" in high_scored_terms

        ranking = pdf_stylings.pages[5].ranking
        assert ranking_is_ordered(ranking)
        high_scored_terms = get_high_scored_terms(ranking)
        assert "5-layer architecture" in high_scored_terms
        assert "method layer" in high_scored_terms
        assert "styling layer" in high_scored_terms

        ranking = pdf_stylings.pages[6].ranking
        assert ranking_is_ordered(ranking)
        high_scored_terms = get_high_scored_terms(ranking)
        assert "5-layer architecture" in high_scored_terms
        assert "technical term layer" in high_scored_terms

    @classmethod
    def assert_pdf_techterms(cls, pdf_techterms: PDFTechnicalTermList) -> None:
        assert pdf_techterms.pdf_path == cls.PDF_PATH
        assert len(pdf_techterms.pages) == 7

        actual_terms = set(map(lambda t: t.term, pdf_techterms.pages[0].terms))
        assert "py-pdf-term" in actual_terms

        actual_terms = set(map(lambda t: t.term, pdf_techterms.pages[1].terms))
        assert "Motivation" in actual_terms

        actual_terms = set(map(lambda t: t.term, pdf_techterms.pages[2].terms))
        assert "Features" in actual_terms

        actual_terms = set(map(lambda t: t.term, pdf_techterms.pages[3].terms))
        assert "Features" in actual_terms

        actual_terms = set(map(lambda t: t.term, pdf_techterms.pages[4].terms))
        assert "5-layers architecture" in actual_terms

        actual_terms = set(map(lambda t: t.term, pdf_techterms.pages[5].terms))
        assert "5-layers architecture" in actual_terms

        actual_terms = set(map(lambda t: t.term, pdf_techterms.pages[6].terms))
        assert "5-layers architecture" in actual_terms


class WikipediaPDFFixture:
    PDF_NAME = "wikipedia-pdf.pdf"
    XML_NAME = "wikipedia-pdf.xml"
    CANDIDATE_NAME = "wikipedia-pdf-candidate.json"

    PDF_PATH = path.join(FIXTURES_DIR, PDF_NAME)
    XML_PATH = path.join(FIXTURES_DIR, XML_NAME)
    CANDIDATE_PATH = path.join(FIXTURES_DIR, CANDIDATE_NAME)
