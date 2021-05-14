from statistics import mean, stdev
from math import exp

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
        if not page_candidates_dict:
            return PageStylingScoreList(page_candidates.page_num, [])
        if len(page_candidates_dict) == 1:
            candidate_str = list(page_candidates_dict.keys())[0]
            scored_term = ScoredTerm(candidate_str, 1.0)
            return PageStylingScoreList(page_candidates.page_num, [scored_term])

        fontsize_mean = mean(
            map(lambda candidate: candidate.fontsize, page_candidates_dict.values())
        )
        fontsize_stdev = stdev(
            map(lambda candidate: candidate.fontsize, page_candidates_dict.values()),
            fontsize_mean,
        )

        def calculate_score(candidate: Term) -> ScoredTerm:
            if fontsize_stdev == 0.0:
                return ScoredTerm(str(candidate), 1.0)

            z = (candidate.fontsize - fontsize_mean) / fontsize_stdev
            score = 2 / (1 + exp(-z))
            return ScoredTerm(str(candidate), score)

        ranking = list(map(calculate_score, page_candidates_dict.values()))
        ranking.sort(key=lambda term: -term.score)
        return PageStylingScoreList(page_candidates.page_num, ranking)
