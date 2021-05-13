from .data import (
    DomainTechnicalTermList,
    PDFTechnicalTermList,
    PageTechnicalTermList,
)
from py_slides_term.candidates import (
    DomainCandidateTermList,
    PDFCandidateTermList,
    PageCandidateTermList,
)
from py_slides_term.methods import MethodTermRanking
from py_slides_term.stylings import (
    DomainStylingScoreList,
    PDFStylingScoreList,
    PageStylingScoreList,
)
from py_slides_term.share.utils import list_remove_dup, ranking_to_dict
from py_slides_term.share.data import ScoredTerm


class TechnicalTermExtractor:
    # public
    def __init__(self, max_num_terms: int = 14, acceptance_rate: float = 0.75):
        self._max_num_terms = max_num_terms
        self._acceptance_rate = acceptance_rate

    def extract_from_domain(
        self,
        domain_candidates: DomainCandidateTermList,
        method_term_ranking: MethodTermRanking,
        domain_styling_scores: DomainStylingScoreList,
    ) -> DomainTechnicalTermList:
        pdf_techterms = [
            self.extract_from_pdf(
                pdf_candidates, method_term_ranking, pdf_styling_scores
            )
            for pdf_candidates, pdf_styling_scores in zip(
                domain_candidates.pdfs, domain_styling_scores.pdfs
            )
        ]
        return DomainTechnicalTermList(domain_candidates.domain, pdf_techterms)

    def extract_from_pdf(
        self,
        pdf_candidates: PDFCandidateTermList,
        method_term_ranking: MethodTermRanking,
        pdf_styling_scores: PDFStylingScoreList,
    ) -> PDFTechnicalTermList:
        page_techterms = [
            self._extract_from_page(
                page_candidates, method_term_ranking, page_styling_scores
            )
            for page_candidates, page_styling_scores in zip(
                pdf_candidates.pages, pdf_styling_scores.pages
            )
        ]
        return PDFTechnicalTermList(pdf_candidates.pdf_path, page_techterms)

    # private
    def _extract_from_page(
        self,
        page_candidates: PageCandidateTermList,
        term_ranking: MethodTermRanking,
        page_styling_scores: PageStylingScoreList,
    ) -> PageTechnicalTermList:
        method_score_dict = ranking_to_dict(term_ranking.ranking, self._acceptance_rate)
        styling_score_dict = ranking_to_dict(page_styling_scores.ranking)

        def term_score(term: str) -> float:
            method_score = method_score_dict[term]
            styling_score = styling_score_dict[term]
            if method_score >= 0.0:
                return method_score * styling_score
            else:
                return method_score / styling_score

        scored_terms = [
            ScoredTerm(term, term_score(term))
            for term in list_remove_dup(list(map(str, page_candidates.candidates)))
            if term in method_score_dict and term in styling_score_dict
        ]

        if len(scored_terms) > self._max_num_terms:
            scores = list(map(lambda scored_term: scored_term.score, scored_terms))
            scores.sort(reverse=True)
            threshold = scores[self._max_num_terms]
            scored_terms = list(
                filter(lambda scored_term: scored_term.score > threshold, scored_terms)
            )

        return PageTechnicalTermList(page_candidates.page_num, scored_terms)
