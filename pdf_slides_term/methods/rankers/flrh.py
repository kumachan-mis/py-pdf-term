from pdf_slides_term.methods.rankers.base import BaseSingleDomainRanker
from pdf_slides_term.methods.collectors.flrh import FLRHRakingData
from pdf_slides_term.methods.rankers.flr import FLRRanker
from pdf_slides_term.methods.collectors.flr import FLRRakingData
from pdf_slides_term.methods.rankers.hits import HITSRanker, HITSAuthHubData
from pdf_slides_term.methods.collectors.hits import HITSRakingData
from pdf_slides_term.methods.data import DomainTermRanking, ScoredTerm
from pdf_slides_term.candidates.data import DomainCandidateTermList
from pdf_slides_term.share.data import TechnicalTerm


# pyright:reportPrivateUsage=false
# FLRHRanker is a friend of FLRRanker and HITSRanker
class FLRHRanker(BaseSingleDomainRanker[FLRHRakingData]):
    # public
    def __init__(self):
        self._flr_ranker = FLRRanker()
        self._hits_ranker = HITSRanker()

    def rank_terms(
        self, domain_candidates: DomainCandidateTermList, ranking_data: FLRHRakingData
    ) -> DomainTermRanking:
        flr_ranking_data = FLRRakingData(
            ranking_data.term_freq,
            ranking_data.left_freq,
            ranking_data.right_freq,
            ranking_data.term_maxsize,
        )
        hits_ranking_data = HITSRakingData(
            ranking_data.term_freq,
            ranking_data.left_freq,
            ranking_data.right_freq,
            ranking_data.term_maxsize,
        )

        auth_hub_data = self._hits_ranker._create_auth_hub_data(hits_ranking_data)
        domain_candidates_dict = domain_candidates.to_domain_candidate_term_dict()
        ranking = list(
            map(
                lambda candidate: self._calculate_score(
                    candidate, flr_ranking_data, hits_ranking_data, auth_hub_data
                ),
                domain_candidates_dict.candidates.values(),
            )
        )
        ranking.sort(key=lambda term: -term.score)
        return DomainTermRanking(domain_candidates.domain, ranking)

    # public
    def _calculate_score(
        self,
        candidate: TechnicalTerm,
        flr_ranking_data: FLRRakingData,
        hits_ranking_data: HITSRakingData,
        auth_hub_data: HITSAuthHubData,
    ) -> ScoredTerm:
        flr_score = self._flr_ranker._calculate_score(candidate, flr_ranking_data).score
        hits_score = self._hits_ranker._calculate_score(
            candidate, hits_ranking_data, auth_hub_data
        ).score
        return ScoredTerm(str(candidate), flr_score + hits_score)
