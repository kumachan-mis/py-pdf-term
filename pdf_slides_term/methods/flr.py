from math import log10
from dataclasses import dataclass
from typing import Dict

from pdf_slides_term.methods.base import BaseSingleDomainTermRankingMethod
from pdf_slides_term.methods.data import DomainTermRanking, ScoredTerm
from pdf_slides_term.candidates.data import DomainCandidateTermList
from pdf_slides_term.mecab.filter import MeCabMorphemeFilter
from pdf_slides_term.share.data import TechnicalTerm


@dataclass
class FLRScoringData:
    term_frequency: Dict[str, int]
    # brute force counting of term occurrences
    # count even if the term occurs as a part of a phrase
    term_maxsize: Dict[str, float]
    # max fontsize of the term
    # default of this is zero
    morpheme_left_frequency: Dict[str, int]
    # number of morphemes connected to the left of the morpheme
    # this of modifying particle is fixed at zero, since the morpheme is meaningless
    morpheme_right_frequency: Dict[str, int]
    # number of morphemes connected to the right of the morpheme
    # this of modifying particle is fixed at zero, since the morpheme is meaningless


class FLRMethod(BaseSingleDomainTermRankingMethod):
    # public
    def __init__(self):
        super().__init__()
        self._morpheme_filter = MeCabMorphemeFilter()

    def rank_terms(
        self, domain_candidates: DomainCandidateTermList
    ) -> DomainTermRanking:
        scoring_data = self._create_scoring_data(domain_candidates)
        term_ranking = self._create_term_ranking(domain_candidates, scoring_data)
        return term_ranking

    # private
    def _create_scoring_data(
        self, domain_candidates: DomainCandidateTermList
    ) -> FLRScoringData:
        scoring_data = self._init_scoring_data()

        for xml_candidates in domain_candidates.xmls:
            for page_candidates in xml_candidates.pages:
                for candidate in page_candidates.candidates:
                    self._update_scoring_data(scoring_data, candidate)

        return scoring_data

    def _init_scoring_data(self) -> FLRScoringData:
        return FLRScoringData(dict(), dict(), dict(), dict())

    def _update_scoring_data(
        self, scoring_data: FLRScoringData, candidate: TechnicalTerm
    ) -> None:
        if candidate.augmented:
            return

        num_morphemes = len(candidate.morphemes)

        for i in range(num_morphemes):
            for j in range(i + 1, num_morphemes + 1):
                sub_morphemes = candidate.morphemes[i:j]
                sub_candidate = TechnicalTerm(sub_morphemes, candidate.fontsize, True)
                sub_candidate_str = str(sub_candidate)
                scoring_data.term_frequency[sub_candidate_str] = (
                    scoring_data.term_frequency.get(sub_candidate_str, 0) + 1
                )
                scoring_data.term_maxsize[sub_candidate_str] = max(
                    scoring_data.term_maxsize.get(sub_candidate_str, 0),
                    sub_candidate.fontsize,
                )

        for i in range(num_morphemes):
            morpheme = candidate.morphemes[i]
            morpheme_str = str(morpheme)
            if self._morpheme_filter.is_modifying_particle(morpheme):
                continue

            if i > 0:
                left_morpheme = candidate.morphemes[i - 1]
                left_morpheme_str = str(left_morpheme)
                if not self._morpheme_filter.is_modifying_particle(left_morpheme):
                    scoring_data.morpheme_left_frequency[morpheme_str] = (
                        scoring_data.morpheme_left_frequency.get(morpheme_str, 0) + 1
                    )
                    scoring_data.morpheme_right_frequency[left_morpheme_str] = (
                        scoring_data.morpheme_right_frequency.get(left_morpheme_str, 0)
                        + 1
                    )
            if i < num_morphemes - 1:
                right_morpheme = candidate.morphemes[i + 1]
                right_morpheme_str = str(right_morpheme)
                if not self._morpheme_filter.is_modifying_particle(right_morpheme):
                    scoring_data.morpheme_right_frequency[morpheme_str] = (
                        scoring_data.morpheme_right_frequency.get(morpheme_str, 0) + 1
                    )
                    scoring_data.morpheme_left_frequency[right_morpheme_str] = (
                        scoring_data.morpheme_left_frequency.get(right_morpheme_str, 0)
                        + 1
                    )

    def _create_term_ranking(
        self, domain_candidates: DomainCandidateTermList, scoring_data: FLRScoringData
    ) -> DomainTermRanking:
        scored_term_set = set()

        for xml_candidates in domain_candidates.xmls:
            for page_candidates in xml_candidates.pages:
                for candidate in page_candidates.candidates:
                    if str(candidate) in scored_term_set:
                        continue
                    scored_candidate = self._calculate_score(candidate, scoring_data)
                    scored_term_set.add(scored_candidate)

        term_ranking = DomainTermRanking(
            domain_candidates.domain,
            sorted(list(scored_term_set), key=lambda scored_term: -scored_term.score),
        )
        return term_ranking

    def _calculate_score(
        self, candidate: TechnicalTerm, scoring_data: FLRScoringData
    ) -> ScoredTerm:
        candidate_str = str(candidate)
        term_fontsize_score = log10(scoring_data.term_maxsize[candidate_str])
        term_frequency_score = log10(scoring_data.term_frequency[candidate_str])

        concatenation_score = 0.0
        for morpheme in candidate.morphemes:
            morpheme_str = str(morpheme)
            concatenation_score += 0.5 * (
                log10(scoring_data.morpheme_left_frequency.get(morpheme_str, 0) + 1)
                + log10(scoring_data.morpheme_right_frequency.get(morpheme_str, 0) + 1)
            )
        concatenation_score /= len(candidate.morphemes)

        score = term_fontsize_score + term_frequency_score + concatenation_score
        return ScoredTerm(candidate_str, score)
