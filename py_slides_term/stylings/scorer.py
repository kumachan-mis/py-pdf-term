from .data import (
    DomainStylingScoreList,
    PDFStylingScoreList,
    PageStylingScoreList,
)
from py_slides_term.candidates import (
    DomainCandidateTermList,
    PDFCandidateTermList,
    PageCandidateTermList,
)
from py_slides_term.share.utils import extended_log10
from py_slides_term.share.data import ScoredTerm, Term


class StylingScorer:
    # public
    def __init__(self):
        pass

    def score_domain_candidates(
        self, domain_candidates: DomainCandidateTermList
    ) -> DomainStylingScoreList:
        return DomainStylingScoreList(
            domain_candidates.domain,
            list(map(self.score_pdf_candidates, domain_candidates.pdfs)),
        )

    def score_pdf_candidates(
        self, pdf_candidates: PDFCandidateTermList
    ) -> PDFStylingScoreList:
        return PDFStylingScoreList(
            pdf_candidates.pdf_path,
            list(map(self._score_page_candidates, pdf_candidates.pages)),
        )

    # private
    def _score_page_candidates(
        self, page_candidates: PageCandidateTermList
    ) -> PageStylingScoreList:
        page_candidates_dict = page_candidates.to_term_dict()
        ranking = list(
            map(
                lambda candidate: self._calculate_score(candidate),
                page_candidates_dict.values(),
            )
        )
        ranking.sort(key=lambda term: -term.score)
        return PageStylingScoreList(page_candidates.page_num, ranking)

    def _calculate_score(self, candidate: Term) -> ScoredTerm:
        score = extended_log10(candidate.fontsize)
        return ScoredTerm(str(candidate), score)
