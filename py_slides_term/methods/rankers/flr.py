from math import log10

from .base import BaseSingleDomainRanker
from ..rankingdata import FLRRankingData
from ..data import DomainTermRanking, ScoredTerm
from py_slides_term.candidates import DomainCandidateTermList
from py_slides_term.mecab import MeCabMorphemeClassifier, BaseMeCabMorpheme
from py_slides_term.share.data import Term


class FLRRanker(BaseSingleDomainRanker[FLRRankingData]):
    # public
    def __init__(self):
        self._classifier = MeCabMorphemeClassifier()

    def rank_terms(
        self, domain_candidates: DomainCandidateTermList, ranking_data: FLRRankingData
    ) -> DomainTermRanking:
        domain_candidates_dict = domain_candidates.to_domain_candidate_term_dict()
        ranking = list(
            map(
                lambda candidate: self._calculate_score(candidate, ranking_data),
                domain_candidates_dict.candidates.values(),
            )
        )
        ranking.sort(key=lambda term: -term.score)
        return DomainTermRanking(domain_candidates.domain, ranking)

    # private
    def _calculate_score(
        self, candidate: Term, ranking_data: FLRRankingData
    ) -> ScoredTerm:
        candidate_str = str(candidate)
        num_morphemes = len(candidate.morphemes)
        num_meaningless_morphemes = sum(
            map(
                lambda morpheme: 1 if self._is_meaningless_morpheme(morpheme) else 0,
                candidate.morphemes,
            )
        )

        term_maxsize_score = (
            log10(ranking_data.term_maxsize[candidate_str])
            if ranking_data.term_maxsize is not None
            else 0.0
        )
        term_freq_score = log10(ranking_data.term_freq[candidate_str])

        concat_score = 0.0
        for morpheme in candidate.morphemes:
            if self._is_meaningless_morpheme(morpheme):
                continue

            morpheme_str = str(morpheme)
            left_score = sum(ranking_data.left_freq[morpheme_str].values())
            right_score = sum(ranking_data.right_freq[morpheme_str].values())
            concat_score += 0.5 * (log10(left_score + 1) + log10(right_score + 1))

        concat_score /= num_morphemes - num_meaningless_morphemes

        score = term_maxsize_score + term_freq_score + concat_score
        return ScoredTerm(candidate_str, score)

    def _is_meaningless_morpheme(self, morpheme: BaseMeCabMorpheme) -> bool:
        is_modifying_particle = self._classifier.is_modifying_particle(morpheme)
        is_symbol = self._classifier.is_symbol(morpheme)
        return is_modifying_particle or is_symbol
