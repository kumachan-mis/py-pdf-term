from .base import BaseSingleDomainRanker
from ..rankingdata import FLRRankingData
from ..data import MethodTermRanking
from py_pdf_term.candidates import DomainCandidateTermList
from py_pdf_term.tokenizer import Morpheme
from py_pdf_term.tokenizer.langs import (
    JapaneseMorphemeClassifier,
    EnglishMorphemeClassifier,
)
from py_pdf_term._common.data import Term, ScoredTerm
from py_pdf_term._common.extended_math import extended_log10


class FLRRanker(BaseSingleDomainRanker[FLRRankingData]):
    def __init__(self) -> None:
        self._ja_classifier = JapaneseMorphemeClassifier()
        self._en_classifier = EnglishMorphemeClassifier()

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
        ranking.sort(key=lambda term: -term.score)
        return MethodTermRanking(domain_candidates.domain, ranking)

    def _calculate_score(
        self, candidate: Term, ranking_data: FLRRankingData
    ) -> ScoredTerm:
        candidate_lemma = candidate.lemma()
        num_morphemes = len(candidate.morphemes)
        num_meaningless_morphemes = sum(
            map(
                lambda morpheme: 1 if self._is_meaningless_morpheme(morpheme) else 0,
                candidate.morphemes,
            )
        )
        term_freq_score = extended_log10(ranking_data.term_freq.get(candidate_lemma, 0))

        concat_score = 0.0
        for morpheme in candidate.morphemes:
            if self._is_meaningless_morpheme(morpheme):
                continue

            lscore = sum(ranking_data.left_freq.get(morpheme.lemma, dict()).values())
            rscore = sum(ranking_data.right_freq.get(morpheme.lemma, dict()).values())
            concat_score += 0.5 * (extended_log10(lscore) + extended_log10(rscore))

        concat_score /= num_morphemes - num_meaningless_morphemes

        score = term_freq_score + concat_score
        return ScoredTerm(candidate_lemma, score)

    def _is_meaningless_morpheme(self, morpheme: Morpheme) -> bool:
        is_ja_meaningless = self._ja_classifier.is_meaningless(morpheme)
        is_en_meaningless = self._en_classifier.is_meaningless(morpheme)
        return is_ja_meaningless or is_en_meaningless
