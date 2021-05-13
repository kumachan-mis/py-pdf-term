from math import log10
from typing import List, Literal

from .base import BaseMultiDomainRanker
from ..rankingdata import LFIDFRankingData
from ..data import MethodTermRanking
from py_slides_term.candidates import DomainCandidateTermList
from py_slides_term.share.data import Term, ScoredTerm, LinguSeq
from py_slides_term.share.utils import extended_log10


class LFIDFRanker(BaseMultiDomainRanker[LFIDFRankingData]):
    # public
    def __init__(
        self,
        tfmode: Literal["natural", "log", "augmented", "logave", "binary"] = "log",
        idfmode: Literal["natural", "smooth", "prob", "unary"] = "natural",
    ):
        self._tfmode = tfmode
        self._idfmode = idfmode

    def rank_terms(
        self,
        domain_candidates: DomainCandidateTermList,
        ranking_data_list: List[LFIDFRankingData],
    ) -> MethodTermRanking:
        domain_candidates_dict = domain_candidates.to_term_dict()
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
        candidate_str = str(candidate)
        lingu_seq = candidate.linguistic_sequence()

        lf = self._calculate_lf(lingu_seq, ranking_data, ranking_data_list)
        idf = self._calculate_idf(lingu_seq, ranking_data, ranking_data_list)
        score = extended_log10(lf * idf)
        return ScoredTerm(candidate_str, score)

    def _calculate_lf(
        self,
        lingu_seq: LinguSeq,
        ranking_data: LFIDFRankingData,
        ranking_data_list: List[LFIDFRankingData],
    ) -> float:
        lf = ranking_data.lingu_freq[lingu_seq]
        max_lf = max(
            map(lambda data: data.lingu_freq.get(lingu_seq, 0), ranking_data_list)
        )
        lf_sum = sum(
            map(lambda data: data.lingu_freq.get(lingu_seq, 0), ranking_data_list)
        )
        ave_lf = lf_sum / len(ranking_data_list)

        if self._idfmode == "natural":
            return lf
        elif self._tfmode == "log":
            return 1.0 * log10(lf) if lf > 0.0 else 0.0
        elif self._tfmode == "augmented":
            return 0.5 + 0.5 * lf / max_lf
        elif self._tfmode == "logave":
            return (1.0 + log10(lf)) / (1.0 + log10(ave_lf)) if lf > 0.0 else 0.0
        else:
            return 1.0 if lf > 0.0 else 0.0

    def _calculate_idf(
        self,
        lingu_seq: LinguSeq,
        ranking_data: LFIDFRankingData,
        ranking_data_list: List[LFIDFRankingData],
    ) -> float:
        num_docs = sum(map(lambda data: data.num_docs, ranking_data_list))
        df = sum(map(lambda data: data.doc_freq.get(lingu_seq, 0), ranking_data_list))

        if self._idfmode == "natural":
            return log10(num_docs / df)
        if self._idfmode == "smooth":
            return log10(num_docs / (df + 1)) + 1.0
        elif self._idfmode == "prob":
            return max(log10((num_docs - df) / df), 0.0)
        else:
            return 1.0
