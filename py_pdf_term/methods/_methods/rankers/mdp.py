from typing import Callable, Iterable, List

from py_pdf_term._common.data import ScoredTerm, Term
from py_pdf_term._common.extended_math import extended_log10
from py_pdf_term.candidates import DomainCandidateTermList

from ..data import MethodTermRanking
from ..rankingdata import MDPRankingData
from .base import BaseMultiDomainRanker


class MDPRanker(BaseMultiDomainRanker[MDPRankingData]):
    def __init__(
        self, compile_scores: Callable[[Iterable[float]], float] = min
    ) -> None:
        self._compile_scores = compile_scores

    def rank_terms(
        self,
        domain_candidates: DomainCandidateTermList,
        ranking_data_list: List[MDPRankingData],
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
        ranking.sort(key=lambda term: -term.score)
        return MethodTermRanking(domain_candidates.domain, ranking)

    def _calculate_score(
        self,
        candidate: Term,
        ranking_data: MDPRankingData,
        other_ranking_data_list: List[MDPRankingData],
    ) -> ScoredTerm:
        candidate_lemma = candidate.lemma()
        score = self._compile_scores(
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

        our_term_freq = our_ranking_data.term_freq.get(candidate_lemma, 0)
        their_term_freq = their_ranking_data.term_freq.get(candidate_lemma, 0)

        our_inum_terms = 1 / our_ranking_data.num_terms
        their_inum_terms = 1 / their_ranking_data.num_terms

        our_term_prob = our_term_freq / our_ranking_data.num_terms
        their_term_prob = their_term_freq / their_ranking_data.num_terms

        term_prob = (our_term_freq + their_term_freq) / (
            our_ranking_data.num_terms + their_ranking_data.num_terms
        )

        return extended_log10(
            (our_term_prob - their_term_prob)
            / (term_prob * (1.0 - term_prob) * (our_inum_terms + their_inum_terms))
        )
