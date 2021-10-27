from math import log10
from typing import List

from py_pdf_term._common.data import LinguSeq, ScoredTerm, Term
from py_pdf_term.candidates import DomainCandidateTermList

from ..data import MethodTermRanking
from ..rankingdata import LFIDFRankingData
from .base import BaseMultiDomainRanker


class LFIDFRanker(BaseMultiDomainRanker[LFIDFRankingData]):
    def __init__(self, lfmode: str = "log", idfmode: str = "natural") -> None:
        self._lfmode = lfmode
        self._idfmode = idfmode

    def rank_terms(
        self,
        domain_candidates: DomainCandidateTermList,
        ranking_data_list: List[LFIDFRankingData],
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
        ranking_data: LFIDFRankingData,
        ranking_data_list: List[LFIDFRankingData],
    ) -> ScoredTerm:
        candidate_lemma = candidate.lemma()
        lingu_seq = candidate.linguistic_sequence()

        lf = self._calculate_lf(lingu_seq, ranking_data, ranking_data_list)
        idf = self._calculate_idf(lingu_seq, ranking_data, ranking_data_list)
        score = log10(lf * idf + 1.0)
        return ScoredTerm(candidate_lemma, score)

    def _calculate_lf(
        self,
        lingu_seq: LinguSeq,
        ranking_data: LFIDFRankingData,
        ranking_data_list: List[LFIDFRankingData],
    ) -> float:
        lf = ranking_data.lingu_freq.get(lingu_seq, 0)

        if self._idfmode == "natural":
            return lf

        elif self._lfmode == "log":
            return 1.0 * log10(lf) if lf > 0 else 0.0

        elif self._lfmode == "augmented":
            max_lf = max(
                map(lambda data: data.lingu_freq.get(lingu_seq, 0), ranking_data_list)
            )
            return 0.5 + 0.5 * lf / max_lf if max_lf > 0 else 0.0

        elif self._lfmode == "logave":
            ave_lf = sum(
                map(lambda data: data.lingu_freq.get(lingu_seq, 0), ranking_data_list)
            ) / len(ranking_data_list)
            return (
                (1.0 + log10(lf)) / (1.0 + log10(ave_lf))
                if lf > 0 and ave_lf > 0.0
                else 0.0
            )

        elif self._lfmode == "binary":
            return 1.0 if lf > 0 else 0.0

        raise ValueError(f"unknown lfmode {self._lfmode}")

    def _calculate_idf(
        self,
        lingu_seq: LinguSeq,
        ranking_data: LFIDFRankingData,
        ranking_data_list: List[LFIDFRankingData],
    ) -> float:
        num_docs = sum(map(lambda data: data.num_docs, ranking_data_list))
        df = sum(map(lambda data: data.doc_freq.get(lingu_seq, 0), ranking_data_list))

        if self._idfmode == "natural":
            return log10(num_docs / df) if df > 0 else 0.0

        if self._idfmode == "smooth":
            return log10(num_docs / (df + 1)) + 1.0

        elif self._idfmode == "prob":
            return max(log10((num_docs - df) / df), 0.0) if df > 0 else 0.0

        elif self._idfmode == "unary":
            return 1.0

        raise ValueError(f"unknown idfmode {self._idfmode}")
