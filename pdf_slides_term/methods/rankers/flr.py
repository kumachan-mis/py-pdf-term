from math import log10
from dataclasses import dataclass
from typing import Dict

from pdf_slides_term.methods.data import DomainTermRanking, ScoredTerm
from pdf_slides_term.candidates.data import DomainCandidateTermList
from pdf_slides_term.share.data import TechnicalTerm


@dataclass
class FLRRakingData:
    term_freq: Dict[str, int]
    term_maxsize: Dict[str, float]
    left_freq: Dict[str, Dict[str, int]]
    right_freq: Dict[str, Dict[str, int]]


class FLRRanker:
    def rank_terms(
        self, domain_candidates: DomainCandidateTermList, ranking_data: FLRRakingData
    ) -> DomainTermRanking:
        scored_term_dict = dict()

        for xml_candidates in domain_candidates.xmls:
            for page_candidates in xml_candidates.pages:
                for candidate in page_candidates.candidates:
                    if str(candidate) in scored_term_dict:
                        continue
                    scored_candidate = self._calculate_score(candidate, ranking_data)
                    scored_term_dict[scored_candidate.term] = scored_candidate

        ranking = sorted(list(scored_term_dict.values()), key=lambda term: -term.score)
        return DomainTermRanking(domain_candidates.domain, ranking)

    def _calculate_score(
        self, candidate: TechnicalTerm, ranking_data: FLRRakingData
    ) -> ScoredTerm:
        candidate_str = str(candidate)

        term_maxsize_score = log10(ranking_data.term_maxsize[candidate_str])
        term_freq_score = log10(ranking_data.term_freq[candidate_str])

        empty = dict()
        concat_score = 0.0
        for morpheme in candidate.morphemes:
            morpheme_str = str(morpheme)
            left_score = sum(ranking_data.left_freq.get(morpheme_str, empty).values())
            right_score = sum(ranking_data.right_freq.get(morpheme_str, empty).values())
            concat_score += 0.5 * (log10(left_score + 1) + log10(right_score + 1))

        concat_score /= len(candidate.morphemes)

        score = term_maxsize_score + term_freq_score + concat_score
        return ScoredTerm(candidate_str, score)
