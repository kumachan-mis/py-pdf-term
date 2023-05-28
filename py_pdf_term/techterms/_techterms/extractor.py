from py_pdf_term._common.data import ScoredTerm
from py_pdf_term.candidates import (
    DomainCandidateTermList,
    PageCandidateTermList,
    PDFCandidateTermList,
)
from py_pdf_term.methods import MethodTermRanking
from py_pdf_term.stylings import (
    DomainStylingScoreList,
    PageStylingScoreList,
    PDFStylingScoreList,
)

from .data import DomainTechnicalTermList, PageTechnicalTermList, PDFTechnicalTermList
from .utils import ranking_to_dict


class TechnicalTermExtractor:
    """Technical term extrator based on ranking method scores and styling scores.

    Args
    ----
        max_num_terms:
            Maximum number of terms in a page of a PDF file to be extracted. The N-best
            candidates are extracted as technical terms. The default value is 10.
        acceptance_rate:
            Acceptance rate of the ranking method scores. The candidates whose
            ranking method scores are lower than the acceptance rate are filtered out
            even if they are in the N-best candidates. The default value is 0.75.
    """

    def __init__(self, max_num_terms: int = 10, acceptance_rate: float = 0.75) -> None:
        if max_num_terms <= 0:
            raise ValueError("max_num_terms must be positive")
        if acceptance_rate <= 0.0 or acceptance_rate > 1.0:
            raise ValueError("acceptance_rate must be in (0.0, 1.0]")

        self._max_num_terms = max_num_terms
        self._acceptance_rate = acceptance_rate
        self._cache: dict[str, float] | None = None

    def extract_from_domain(
        self,
        domain_candidates: DomainCandidateTermList,
        term_ranking: MethodTermRanking,
        domain_styling_scores: DomainStylingScoreList,
    ) -> DomainTechnicalTermList:
        """Extract tecnical terms in PDF files in a domain. The terms are sorted in
        appearance order, not in score order.

        Args
        ----
            domain_candidates:
                List of candidate terms in a domain. The target of extraction.
            term_ranking:
                Ranking method scores for each candidate term in a domain.
            domain_styling_scores:
                Styling scores for each candidate term in a domain.

        Returns
        -------
            DomainTechnicalTermList:
                List of technical terms in PDF files in a domain. The terms are sorted
                in appearance order, not in score order.
        """

        cache_should_flush = self._cache is None
        if self._cache is None:
            self._cache = ranking_to_dict(term_ranking.ranking, self._acceptance_rate)

        pdf_techterms = [
            self.extract_from_pdf(pdf_candidates, term_ranking, pdf_styling_scores)
            for pdf_candidates, pdf_styling_scores in zip(
                domain_candidates.pdfs, domain_styling_scores.pdfs
            )
        ]

        if cache_should_flush:
            self._cache = None

        return DomainTechnicalTermList(domain_candidates.domain, pdf_techterms)

    def extract_from_pdf(
        self,
        pdf_candidates: PDFCandidateTermList,
        term_ranking: MethodTermRanking,
        pdf_styling_scores: PDFStylingScoreList,
    ) -> PDFTechnicalTermList:
        """Extract tecnical terms in a PDF file. The terms are sorted in appearance
        order, not in score order.

        Args
        ----
            pdf_candidates:
                List of candidate terms in a PDF file. The target of extraction.
            term_ranking:
                Ranking method scores for each candidate term in a domain.
            pdf_styling_scores:
                Styling scores for each candidate term in a PDF file.

        Returns
        -------
            PDFTechnicalTermList:
                List of technical terms in a PDF file. The terms are sorted in
                appearance order, not in score order.
        """

        cache_should_flush = self._cache is None
        if self._cache is None:
            self._cache = ranking_to_dict(term_ranking.ranking, self._acceptance_rate)

        page_techterms = [
            self._extract_from_page(page_candidates, term_ranking, page_styling_scores)
            for page_candidates, page_styling_scores in zip(
                pdf_candidates.pages, pdf_styling_scores.pages
            )
        ]

        if cache_should_flush:
            self._cache = None

        return PDFTechnicalTermList(pdf_candidates.pdf_path, page_techterms)

    def _extract_from_page(
        self,
        page_candidates: PageCandidateTermList,
        term_ranking: MethodTermRanking,
        page_styling_scores: PageStylingScoreList,
    ) -> PageTechnicalTermList:
        cache_should_flush = self._cache is None
        if self._cache is None:
            self._cache = ranking_to_dict(term_ranking.ranking, self._acceptance_rate)

        method_score_dict = self._cache
        styling_score_dict = ranking_to_dict(page_styling_scores.ranking)

        def term_score(term_lemma: str) -> float:
            method_score = method_score_dict[term_lemma]
            styling_score = styling_score_dict[term_lemma]
            if method_score >= 0.0:
                return method_score * styling_score
            else:
                return method_score / styling_score

        scored_terms = [
            ScoredTerm(term_str, term_score(term.lemma()))
            for term_str, term in page_candidates.to_nostyle_candidates_dict().items()
            if term.lemma() in method_score_dict and term.lemma() in styling_score_dict
        ]

        if len(scored_terms) > self._max_num_terms:
            scores = list(map(lambda scored_term: scored_term.score, scored_terms))
            scores.sort(reverse=True)
            threshold = scores[self._max_num_terms]
            scored_terms = list(
                filter(lambda scored_term: scored_term.score > threshold, scored_terms)
            )

        if cache_should_flush:
            self._cache = None

        return PageTechnicalTermList(page_candidates.page_num, scored_terms)
