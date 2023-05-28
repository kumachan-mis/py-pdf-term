from sys import float_info

from py_pdf_term._common.data import ScoredTerm
from py_pdf_term._common.utils import extended_log10
from py_pdf_term.candidates import DomainCandidateTermList
from py_pdf_term.tokenizers import Term

from ..data import MethodTermRanking
from ..rankingdata import MDPRankingData
from .base import BaseMultiDomainRanker


class MDPRanker(BaseMultiDomainRanker[MDPRankingData]):
    """Term ranker by MDP algorithm."""

    def __init__(self) -> None:
        pass

    def rank_terms(
        self,
        domain_candidates: DomainCandidateTermList,
        ranking_data_list: list[MDPRankingData],
    ) -> MethodTermRanking:
        domain_candidates_dict = domain_candidates.to_nostyle_candidates_dict(
            to_str=lambda candidate: candidate.lemma()
        )
        ranking_data = next(
            filter(
                lambda item: item.domain == domain_candidates.domain,
                ranking_data_list,
            )
        )
        other_ranking_data_list = list(
            filter(
                lambda item: item.domain != domain_candidates.domain,
                ranking_data_list,
            )
        )
        ranking = list(
            map(
                lambda candidate: self._calculate_score(
                    candidate, ranking_data, other_ranking_data_list
                ),
                domain_candidates_dict.values(),
            )
        )
        ranking.sort(key=lambda term: term.score, reverse=True)
        return MethodTermRanking(domain_candidates.domain, ranking)

    def _calculate_score(
        self,
        candidate: Term,
        ranking_data: MDPRankingData,
        other_ranking_data_list: list[MDPRankingData],
    ) -> ScoredTerm:
        candidate_lemma = candidate.lemma()
        score = min(
            map(
                lambda other_ranking_data: self._calculate_zvalue(
                    candidate, ranking_data, other_ranking_data
                ),
                other_ranking_data_list,
            )
        )

        return ScoredTerm(candidate_lemma, score)

    def _calculate_zvalue(
        self,
        candidate: Term,
        our_ranking_data: MDPRankingData,
        their_ranking_data: MDPRankingData,
    ) -> float:
        candidate_lemma = candidate.lemma()

        num_terms = our_ranking_data.num_terms + their_ranking_data.num_terms

        our_term_freq = our_ranking_data.term_freq.get(candidate_lemma, 0)
        their_term_freq = their_ranking_data.term_freq.get(candidate_lemma, 0)
        term_freq = our_term_freq + their_term_freq

        if term_freq == 0 or term_freq == num_terms:
            return -float_info.max

        our_inum_terms = 1 / our_ranking_data.num_terms
        their_inum_terms = 1 / their_ranking_data.num_terms

        our_term_prob = our_term_freq / our_ranking_data.num_terms
        their_term_prob = their_term_freq / their_ranking_data.num_terms
        term_prob = term_freq / num_terms

        return extended_log10(
            (our_term_prob - their_term_prob)
            / (term_prob * (1.0 - term_prob) * (our_inum_terms + their_inum_terms))
        )
