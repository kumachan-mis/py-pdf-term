from typing import List, Callable, Iterable

from .base import BaseMultiDomainRanker
from ..rankingdata import MDPRankingData
from ..data import DomainTermRanking, ScoredTerm
from py_slides_term.candidates import DomainCandidateTermList
from py_slides_term.share.data import Term
from py_slides_term.share.utils import extended_log10


class MDPRanker(BaseMultiDomainRanker[MDPRankingData]):
    # public
    def __init__(self, compile_scores: Callable[[Iterable[float]], float] = min):
        self._compile_scores = compile_scores

    def rank_terms(
        self,
        domain_candidates: DomainCandidateTermList,
        ranking_data: MDPRankingData,
        other_ranking_data_list: List[MDPRankingData],
    ) -> DomainTermRanking:
        domain_candidates_dict = domain_candidates.to_domain_candidate_term_dict()
        ranking = list(
            map(
                lambda candidate: self._calculate_score(
                    candidate, ranking_data, other_ranking_data_list
                ),
                domain_candidates_dict.candidates.values(),
            )
        )
        ranking.sort(key=lambda term: -term.score)
        return DomainTermRanking(domain_candidates.domain, ranking)

    # private
    def _calculate_score(
        self,
        candidate: Term,
        ranking_data: MDPRankingData,
        other_ranking_data_list: List[MDPRankingData],
    ) -> ScoredTerm:
        score = self._compile_scores(
            map(
                lambda other_ranking_data: self._calculate_zvalue(
                    candidate, ranking_data, other_ranking_data
                ),
                other_ranking_data_list,
            )
        )

        return ScoredTerm(str(candidate), score)

    def _calculate_zvalue(
        self,
        candidate: Term,
        our_ranking_data: MDPRankingData,
        their_ranking_data: MDPRankingData,
    ) -> float:
        candidate_str = str(candidate)

        our_term_maxsize = (
            our_ranking_data.term_maxsize[candidate_str]
            if our_ranking_data.term_maxsize is not None
            else 1.0
        )
        their_term_maxsize = (
            their_ranking_data.term_maxsize.get(candidate_str, 0.0)
            if their_ranking_data.term_maxsize is not None
            else 1.0
        )

        our_term_freq = our_ranking_data.term_freq[candidate_str]
        their_term_freq = their_ranking_data.term_freq.get(candidate_str, 0)

        our_inum_terms = 1 / our_ranking_data.num_terms
        their_inum_terms = 1 / their_ranking_data.num_terms

        our_term_prob = our_term_freq / our_ranking_data.num_terms
        their_term_prob = their_term_freq / their_ranking_data.num_terms
        term_prob = (our_term_freq + their_term_freq) / (
            our_ranking_data.num_terms + their_ranking_data.num_terms
        )

        return extended_log10(
            (our_term_maxsize * our_term_prob - their_term_maxsize * their_term_prob)
            / (term_prob * (1.0 - term_prob) * (our_inum_terms + their_inum_terms))
        )
