from py_pdf_term._common.data import ScoredTerm
from py_pdf_term.candidates import (
    DomainCandidateTermList,
    PageCandidateTermList,
    PDFCandidateTermList,
)

from .data import DomainStylingScoreList, PageStylingScoreList, PDFStylingScoreList
from .scores import BaseStylingScore, ColorScore, FontsizeScore


class StylingScorer:
    """Scorer for styling scores. The styling scores are combined by multiplication of
    each score.

    Args
    ----
        styling_score_clses:
            Styling scorers to be combined. If None, the default scorers are used.
            The default scorers are FontsizeScore and ColorScore.
    """

    def __init__(
        self, styling_score_clses: list[type[BaseStylingScore]] | None = None
    ) -> None:
        if styling_score_clses is None:
            styling_score_clses = [FontsizeScore, ColorScore]

        self._styling_score_clses = styling_score_clses

    def score_domain_candidates(
        self, domain_candidates: DomainCandidateTermList
    ) -> DomainStylingScoreList:
        """Calculate styling scores for each candidate term in a domain.

        Args
        ----
            domain_candidates:
                List of candidate terms in a domain. The target of analysis.

        Returns
        -------
            DomainStylingScoreList:
                List of styling scores for each candidate term in a domain. The
                scores are sorted in descending order.
        """

        return DomainStylingScoreList(
            domain_candidates.domain,
            list(map(self.score_pdf_candidates, domain_candidates.pdfs)),
        )

    def score_pdf_candidates(
        self, pdf_candidates: PDFCandidateTermList
    ) -> PDFStylingScoreList:
        """Calculate styling scores for each candidate term in a PDF file.

        Args
        ----
            pdf_candidates:
                List of candidate terms in a PDF file. The target of analysis.

        Returns
        -------
            PDFStylingScoreList:
                List of styling scores for each candidate term in a PDF file. The
                scores are sorted in descending order.
        """

        return PDFStylingScoreList(
            pdf_candidates.pdf_path,
            list(map(self._score_page_candidates, pdf_candidates.pages)),
        )

    def _score_page_candidates(
        self, page_candidates: PageCandidateTermList
    ) -> PageStylingScoreList:
        styling_scores: dict[str, float] = {
            candidate.lemma(): 1.0 for candidate in page_candidates.candidates
        }

        for styling_score_cls in self._styling_score_clses:
            styling_score = styling_score_cls(page_candidates)

            scores: dict[str, float] = dict()
            for candidate in page_candidates.candidates:
                candidate_lemma = candidate.lemma()
                score = styling_score.calculate_score(candidate)
                if candidate_lemma not in scores or score > scores[candidate_lemma]:
                    scores[candidate_lemma] = score

            for candidate_lemma in styling_scores:
                styling_scores[candidate_lemma] *= scores[candidate_lemma]

        ranking = list(map(lambda item: ScoredTerm(*item), styling_scores.items()))
        ranking.sort(key=lambda scored_term: scored_term.score, reverse=True)
        return PageStylingScoreList(page_candidates.page_num, ranking)
