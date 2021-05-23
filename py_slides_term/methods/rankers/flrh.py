from .base import BaseSingleDomainRanker
from .flr import FLRRanker
from .hits import HITSRanker, HITSAuthHubData
from ..rankingdata import FLRHRankingData, FLRRankingData, HITSRankingData
from ..data import MethodTermRanking
from py_slides_term.candidates import DomainCandidateTermList
from py_slides_term.share.data import Term, ScoredTerm


class FLRHRanker(BaseSingleDomainRanker[FLRHRankingData]):
    # public
    def __init__(self, threshold: float = 1e-8):
        self._flr_ranker = FLRRanker()
        self._hits_ranker = HITSRanker(threshold=threshold)

    # pyright:reportPrivateUsage=false
    # FLRHRanker is a friend of FLRRanker and HITSRanker
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

        auth_hub_data = self._hits_ranker._create_auth_hub_data(hits_ranking_data)
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
        ranking.sort(key=lambda term: -term.score)
        return MethodTermRanking(domain_candidates.domain, ranking)

    # public
    def _calculate_score(
        self,
        candidate: Term,
        flr_ranking_data: FLRRankingData,
        hits_ranking_data: HITSRankingData,
        auth_hub_data: HITSAuthHubData,
    ) -> ScoredTerm:
        candidate_lemma = candidate.lemma()
        flr_score = self._flr_ranker._calculate_score(candidate, flr_ranking_data).score
        hits_score = self._hits_ranker._calculate_score(
            candidate, hits_ranking_data, auth_hub_data
        ).score
        return ScoredTerm(candidate_lemma, flr_score + hits_score)
