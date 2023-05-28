from py_pdf_term._common.data import ScoredTerm
from py_pdf_term.candidates import DomainCandidateTermList
from py_pdf_term.tokenizers import Term

from ..data import MethodTermRanking
from ..rankingdata import FLRHRankingData, FLRRankingData, HITSRankingData
from .base import BaseSingleDomainRanker
from .flr import FLRRanker
from .hits import HITSAuthHubData, HITSRanker


class FLRHRanker(BaseSingleDomainRanker[FLRHRankingData]):
    """Term ranker by FLRH algorithm. This algorithm is a combination of FLR and HITS.

    Args
    ----
        threshold:
            Threshold value for HITS algorithm. The default is 1e-8.
        max_loop:
            Maximum number of loops for HITS algorithm. The default is 1000.
    """

    def __init__(self, threshold: float = 1e-8, max_loop: int = 1000) -> None:
        self._flr_ranker = FLRRanker()
        self._hits_ranker = HITSRanker(threshold=threshold, max_loop=max_loop)

    def rank_terms(
        self, domain_candidates: DomainCandidateTermList, ranking_data: FLRHRankingData
    ) -> MethodTermRanking:
        flr_ranking_data = FLRRankingData(
            ranking_data.domain,
            ranking_data.term_freq,
            ranking_data.left_freq,
            ranking_data.right_freq,
        )
        hits_ranking_data = HITSRankingData(
            ranking_data.domain,
            ranking_data.term_freq,
            ranking_data.left_freq,
            ranking_data.right_freq,
        )

        auth_hub_data = self._hits_ranker._create_auth_hub_data(  # pyright: ignore[reportPrivateUsage] # noqa: E501
            hits_ranking_data
        )
        domain_candidates_dict = domain_candidates.to_nostyle_candidates_dict(
            to_str=lambda candidate: candidate.lemma()
        )
        ranking = list(
            map(
                lambda candidate: self._calculate_score(
                    candidate, flr_ranking_data, hits_ranking_data, auth_hub_data
                ),
                domain_candidates_dict.values(),
            )
        )
        ranking.sort(key=lambda scored_term: scored_term.score, reverse=True)
        return MethodTermRanking(domain_candidates.domain, ranking)

    def _calculate_score(
        self,
        candidate: Term,
        flr_ranking_data: FLRRankingData,
        hits_ranking_data: HITSRankingData,
        auth_hub_data: HITSAuthHubData,
    ) -> ScoredTerm:
        candidate_lemma = candidate.lemma()
        flr_score = self._flr_ranker._calculate_score(  # pyright: ignore[reportPrivateUsage] # noqa: E501
            candidate, flr_ranking_data
        ).score
        hits_score = self._hits_ranker._calculate_score(  # pyright: ignore[reportPrivateUsage] # noqa: E501
            candidate, hits_ranking_data, auth_hub_data
        ).score
        return ScoredTerm(candidate_lemma, flr_score + hits_score)
