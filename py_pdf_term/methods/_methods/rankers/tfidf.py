from math import log10
from typing import List

from py_pdf_term._common.data import ScoredTerm, Term
from py_pdf_term._common.extended_math import extended_log10
from py_pdf_term.candidates import DomainCandidateTermList

from ..data import MethodTermRanking
from ..rankingdata import TFIDFRankingData
from .base import BaseMultiDomainRanker


class TFIDFRanker(BaseMultiDomainRanker[TFIDFRankingData]):
    def __init__(self, tfmode: str = "log", idfmode: str = "natural") -> None:
        self._tfmode = tfmode
        self._idfmode = idfmode

    def rank_terms(
        self,
        domain_candidates: DomainCandidateTermList,
        ranking_data_list: List[TFIDFRankingData],
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
        ranking.sort(key=lambda term: -term.score)
        return MethodTermRanking(domain_candidates.domain, ranking)

    def _calculate_score(
        self,
        candidate: Term,
        ranking_data: TFIDFRankingData,
        ranking_data_list: List[TFIDFRankingData],
    ) -> ScoredTerm:
        candidate_lemma = candidate.lemma()

        tf = self._calculate_tf(candidate_lemma, ranking_data, ranking_data_list)
        idf = self._calculate_idf(candidate_lemma, ranking_data, ranking_data_list)
        score = extended_log10(tf * idf)
        return ScoredTerm(candidate_lemma, score)

    def _calculate_tf(
        self,
        candidate: str,
        ranking_data: TFIDFRankingData,
        ranking_data_list: List[TFIDFRankingData],
    ) -> float:
        tf = ranking_data.term_freq.get(candidate, 0)

        if self._idfmode == "natural":
            return tf

        elif self._tfmode == "log":
            return 1.0 * log10(tf) if tf > 0 else 0.0

        elif self._tfmode == "augmented":
            max_tf = max(
                map(lambda data: data.term_freq.get(candidate, 0), ranking_data_list)
            )
            return 0.5 + 0.5 * tf / max_tf if max_tf > 0 else 0.0

        elif self._tfmode == "logave":
            ave_tf = sum(
                map(lambda data: data.term_freq.get(candidate, 0), ranking_data_list)
            ) / len(ranking_data_list)
            return (
                (1.0 + log10(tf)) / (1.0 + log10(ave_tf))
                if tf > 0 and ave_tf > 0.0
                else 0.0
            )

        elif self._tfmode == "binary":
            return 1.0 if tf > 0 else 0.0

        raise ValueError(f"unknown tfmode {self._tfmode}")

    def _calculate_idf(
        self,
        candidate: str,
        ranking_data: TFIDFRankingData,
        ranking_data_list: List[TFIDFRankingData],
    ) -> float:
        num_docs = sum(map(lambda data: data.num_docs, ranking_data_list))
        df = sum(map(lambda data: data.doc_freq.get(candidate, 0), ranking_data_list))

        if self._idfmode == "natural":
            return log10(num_docs / df) if df > 0 else 0.0

        if self._idfmode == "smooth":
            return log10(num_docs / (df + 1)) + 1.0

        elif self._idfmode == "prob":
            return max(log10((num_docs - df) / df), 0.0) if df > 0 else 0.0

        elif self._idfmode == "unary":
            return 1.0

        raise ValueError(f"unknown idfmode {self._idfmode}")
