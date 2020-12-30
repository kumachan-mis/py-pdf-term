from math import log10
from dataclasses import dataclass
from typing import List, Dict, Optional, Literal

from pdf_slides_term.methods.data import DomainTermRanking, ScoredTerm
from pdf_slides_term.candidates.data import DomainCandidateTermList
from pdf_slides_term.share.data import TechnicalTerm


@dataclass(frozen=True)
class TFIDFDomainRankingData:
    domain: str
    # unique domain name
    term_freq: Dict[str, int]
    # brute force counting of term occurrences in the domain
    # count even if the term occurs as a part of a phrase
    doc_freq: Dict[str, int]
    # number of documents in the domain that contain the term
    # count even if the term occurs as a part of a phrase
    num_docs: int
    # number of documents in the domain
    term_maxsize: Optional[Dict[str, float]] = None
    # max fontsize of the term in the domain
    # default of this is zero


class TFIDFRanker:
    # public
    def __init__(
        self,
        tf_mode: Literal["natural", "log", "augmented", "logave", "binary"] = "log",
        idf_mode: Literal["natural", "smooth", "prob", "unary"] = "natural",
    ):
        self._tf_mode = tf_mode
        self._idf_mode = idf_mode

    def rank_terms(
        self,
        domain_candidates: DomainCandidateTermList,
        ranking_data: TFIDFDomainRankingData,
        other_ranking_data_list: List[TFIDFDomainRankingData],
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

    def _calculate_score(
        self,
        candidate: TechnicalTerm,
        ranking_data: TFIDFDomainRankingData,
        other_ranking_data_list: List[TFIDFDomainRankingData],
    ) -> ScoredTerm:
        candidate_str = str(candidate)

        tf = self._calculate_tf(candidate_str, ranking_data, other_ranking_data_list)
        idf = self._calculate_idf(candidate_str, ranking_data, other_ranking_data_list)
        term_maxsize = (
            ranking_data.term_maxsize[candidate_str]
            if ranking_data.term_maxsize is not None
            else 1.0
        )
        score = log10(term_maxsize * tf * idf)
        return ScoredTerm(str(candidate), score)

    def _calculate_tf(
        self,
        candidate_str: str,
        ranking_data: TFIDFDomainRankingData,
        other_ranking_data_list: List[TFIDFDomainRankingData],
    ) -> float:
        all_data = [ranking_data] + other_ranking_data_list

        tf = ranking_data.term_freq[candidate_str]
        max_tf = max(map(lambda data: data.term_freq.get(candidate_str, 0), all_data))
        tf_sum = sum(map(lambda data: data.term_freq.get(candidate_str, 0), all_data))
        ave_tf = tf_sum / len(all_data)

        if self._idf_mode == "natural":
            return tf
        elif self._tf_mode == "log":
            return 1.0 * log10(tf) if tf > 0.0 else 0.0
        elif self._tf_mode == "augmented":
            return 0.5 + 0.5 * tf / max_tf
        elif self._tf_mode == "logave":
            return (1.0 + log10(tf)) / (1.0 + log10(ave_tf)) if tf > 0.0 else 0.0
        else:
            return 1.0 if tf > 0.0 else 0.0

    def _calculate_idf(
        self,
        candidate_str: str,
        ranking_data: TFIDFDomainRankingData,
        other_ranking_data_list: List[TFIDFDomainRankingData],
    ) -> float:
        all_data = [ranking_data] + other_ranking_data_list

        num_docs = sum(map(lambda data: data.num_docs, all_data))
        df = sum(map(lambda data: data.doc_freq.get(candidate_str, 0), all_data))

        if self._idf_mode == "natural":
            return log10(num_docs / df)
        if self._idf_mode == "smooth":
            return log10(num_docs / (df + 1)) + 1.0
        elif self._idf_mode == "prob":
            return max(log10((num_docs - df) / df), 0.0)
        else:
            return 1.0
