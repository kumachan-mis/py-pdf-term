from py_pdf_term._common.data import ScoredTerm, Term
from py_pdf_term._common.extended_math import extended_log10
from py_pdf_term.candidates import DomainCandidateTermList

from ..data import MethodTermRanking
from ..rankingdata import MCValueRankingData
from .base import BaseSingleDomainRanker


class MCValueRanker(BaseSingleDomainRanker[MCValueRankingData]):
    def __init__(self) -> None:
        pass

    def rank_terms(
        self,
        domain_candidates: DomainCandidateTermList,
        ranking_data: MCValueRankingData,
    ) -> MethodTermRanking:
        domain_candidates_dict = domain_candidates.to_nostyle_candidates_dict(
            to_str=lambda candidate: candidate.lemma()
        )
        ranking = list(
            map(
                lambda candidate: self._calculate_score(candidate, ranking_data),
                domain_candidates_dict.values(),
            )
        )
        ranking.sort(key=lambda term: -term.score)
        return MethodTermRanking(domain_candidates.domain, ranking)

    def _calculate_score(
        self, candidate: Term, ranking_data: MCValueRankingData
    ) -> ScoredTerm:
        candidate_lemma = candidate.lemma()

        term_freq = ranking_data.term_freq.get(candidate_lemma, 0)
        container_terms = ranking_data.container_terms.get(candidate_lemma, set())
        num_containers = len(container_terms)
        container_freq = sum(
            map(
                lambda container: ranking_data.term_freq.get(container, 0),
                container_terms,
            )
        )

        term_len_score = extended_log10(len(candidate.tokens))
        freq_score = extended_log10(
            term_freq - container_freq / num_containers
            if num_containers > 0
            else term_freq
        )
        score = term_len_score + freq_score
        return ScoredTerm(candidate_lemma, score)
