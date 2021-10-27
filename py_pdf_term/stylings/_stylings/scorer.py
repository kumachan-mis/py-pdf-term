from typing import Dict, List, Optional, Type

from py_pdf_term._common.data import ScoredTerm
from py_pdf_term.candidates import (
    DomainCandidateTermList,
    PageCandidateTermList,
    PDFCandidateTermList,
)

from .data import DomainStylingScoreList, PageStylingScoreList, PDFStylingScoreList
from .scores import BaseStylingScore, ColorScore, FontsizeScore


class StylingScorer:
    def __init__(
        self, styling_score_clses: Optional[List[Type[BaseStylingScore]]] = None
    ) -> None:
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

    def _score_page_candidates(
        self, page_candidates: PageCandidateTermList
    ) -> PageStylingScoreList:
        styling_scores: Dict[str, float] = {
            candidate.lemma(): 1.0 for candidate in page_candidates.candidates
        }

        for styling_score_cls in self._styling_score_clses:
            styling_score = styling_score_cls(page_candidates)

            scores: Dict[str, float] = dict()
            for candidate in page_candidates.candidates:
                candidate_lemma = candidate.lemma()
                score = styling_score.calculate_score(candidate)
                if candidate_lemma not in scores or score > scores[candidate_lemma]:
                    scores[candidate_lemma] = score

            for candidate_lemma in styling_scores:
                styling_scores[candidate_lemma] *= scores[candidate_lemma]

        ranking = list(map(lambda item: ScoredTerm(*item), styling_scores.items()))
        ranking.sort(key=lambda scored_term: -scored_term.score)
        return PageStylingScoreList(page_candidates.page_num, ranking)
