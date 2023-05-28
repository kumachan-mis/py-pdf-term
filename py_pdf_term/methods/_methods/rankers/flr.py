from py_pdf_term._common.data import ScoredTerm
from py_pdf_term._common.utils import extended_log10
from py_pdf_term.candidates import DomainCandidateTermList
from py_pdf_term.tokenizers import Term

from ..data import MethodTermRanking
from ..rankingdata import FLRRankingData
from .base import BaseSingleDomainRanker


class FLRRanker(BaseSingleDomainRanker[FLRRankingData]):
    """Term ranker by FLR algorithm."""

    def __init__(self) -> None:
        pass

    def rank_terms(
        self, domain_candidates: DomainCandidateTermList, ranking_data: FLRRankingData
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
        ranking.sort(key=lambda term: term.score, reverse=True)
        return MethodTermRanking(domain_candidates.domain, ranking)

    def _calculate_score(
        self, candidate: Term, ranking_data: FLRRankingData
    ) -> ScoredTerm:
        candidate_lemma = candidate.lemma()
        num_tokens = len(candidate.tokens)
        num_meaningless_tokens = sum(
            map(lambda token: 1 if token.is_meaningless else 0, candidate.tokens)
        )
        term_freq_score = extended_log10(ranking_data.term_freq.get(candidate_lemma, 0))

        concat_score = 0.0
        for token in candidate.tokens:
            if token.is_meaningless:
                continue

            lscore = sum(ranking_data.left_freq.get(token.lemma, dict()).values())
            rscore = sum(ranking_data.right_freq.get(token.lemma, dict()).values())
            concat_score += 0.5 * (extended_log10(lscore) + extended_log10(rscore))

        concat_score /= num_tokens - num_meaningless_tokens

        score = term_freq_score + concat_score
        return ScoredTerm(candidate_lemma, score)
