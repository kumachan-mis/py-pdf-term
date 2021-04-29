from math import log10
from .base import BaseSingleDomainRanker
from ..rankingdata import MCValueRankingData
from ..data import DomainTermRanking
from py_slides_term.candidates import DomainCandidateTermList
from py_slides_term.share.data import Term, ScoredTerm
from py_slides_term.share.utils import extended_log10


class MCValueRanker(BaseSingleDomainRanker[MCValueRankingData]):
    # public
    def __init__(self):
        pass

    def rank_terms(
        self,
        domain_candidates: DomainCandidateTermList,
        ranking_data: MCValueRankingData,
    ) -> DomainTermRanking:
        domain_candidates_dict = domain_candidates.to_domain_candidate_term_dict()
        ranking = list(
            map(
                lambda candidate: self._calculate_score(candidate, ranking_data),
                domain_candidates_dict.candidates.values(),
            )
        )
        ranking.sort(key=lambda term: -term.score)
        return DomainTermRanking(domain_candidates.domain, ranking)

    # private
    def _calculate_score(
        self, candidate: Term, ranking_data: MCValueRankingData
    ) -> ScoredTerm:
        candidate_str = str(candidate)

        term_freq = ranking_data.term_freq[candidate_str]
        container_terms = ranking_data.container_terms[candidate_str]
        num_containers = len(container_terms)
        container_freq = sum(
            map(
                lambda container: ranking_data.term_freq[container],
                container_terms,
            )
        )

        term_len_score = log10(len(candidate.morphemes))
        freq_score = extended_log10(
            term_freq - container_freq / num_containers
            if num_containers > 0
            else term_freq
        )
        term_maxsize_score = (
            log10(ranking_data.term_maxsize[candidate_str])
            if ranking_data.term_maxsize is not None
            else 0.0
        )

        score = term_len_score + freq_score + term_maxsize_score
        return ScoredTerm(candidate_str, score)
