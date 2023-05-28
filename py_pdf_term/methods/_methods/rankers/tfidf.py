from math import log10

from py_pdf_term._common.data import ScoredTerm
from py_pdf_term._common.utils import extended_log10
from py_pdf_term.candidates import DomainCandidateTermList
from py_pdf_term.tokenizers import Term

from ..data import MethodTermRanking
from ..rankingdata import TFIDFRankingData
from .base import BaseMultiDomainRanker


class TFIDFRanker(BaseMultiDomainRanker[TFIDFRankingData]):
    """Term ranker by TF-IDF algorithm."""

    def __init__(self) -> None:
        pass

    def rank_terms(
        self,
        domain_candidates: DomainCandidateTermList,
        ranking_data_list: list[TFIDFRankingData],
    ) -> MethodTermRanking:
        domain_candidates_dict = domain_candidates.to_nostyle_candidates_dict()
        ranking_data = next(
            filter(
                lambda item: item.domain == domain_candidates.domain,
                ranking_data_list,
            )
        )
        ranking = list(
            map(
                lambda candidate: self._calculate_score(
                    candidate, ranking_data, ranking_data_list
                ),
                domain_candidates_dict.values(),
            )
        )
        ranking.sort(key=lambda term: term.score, reverse=True)
        return MethodTermRanking(domain_candidates.domain, ranking)

    def _calculate_score(
        self,
        candidate: Term,
        ranking_data: TFIDFRankingData,
        ranking_data_list: list[TFIDFRankingData],
    ) -> ScoredTerm:
        candidate_lemma = candidate.lemma()

        tf = ranking_data.term_freq.get(candidate_lemma, 0)
        log_tf = log10(tf) if tf > 0 else 0.0

        num_docs = sum(map(lambda data: data.num_docs, ranking_data_list))
        df = sum(
            map(lambda data: data.doc_freq.get(candidate_lemma, 0), ranking_data_list)
        )
        log_idf = log10(num_docs / df) if df > 0 else 0.0

        score = extended_log10(log_tf * log_idf)
        return ScoredTerm(candidate_lemma, score)
