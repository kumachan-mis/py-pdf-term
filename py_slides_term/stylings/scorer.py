from typing import List, Dict, Optional, Type

from .scores import BaseStylingScore, FontsizeScore, ColorScore
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
from py_slides_term.share.data import ScoredTerm


class StylingScorer:
    # public
    def __init__(
        self, styling_score_clses: Optional[List[Type[BaseStylingScore]]] = None
    ):
        if styling_score_clses is None:
            styling_score_clses = [FontsizeScore, ColorScore]

        self._styling_score_clses = styling_score_clses

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
        styling_scores: Dict[str, float] = {
            str(candidate): 1.0 for candidate in page_candidates.candidates
        }

        for styling_score_cls in self._styling_score_clses:
            styling_score = styling_score_cls(page_candidates)

            scores: Dict[str, float] = dict()
            for candidate in page_candidates.candidates:
                candidate_str = str(candidate)
                score = styling_score.calculate_score(candidate)
                if candidate_str not in scores or score > scores[candidate_str]:
                    scores[candidate_str] = score

            for candidate_str in styling_scores:
                styling_scores[candidate_str] *= scores[candidate_str]

        ranking = list(map(lambda item: ScoredTerm(*item), styling_scores.items()))
        ranking.sort(key=lambda scored_term: -scored_term.score)
        return PageStylingScoreList(page_candidates.page_num, ranking)
