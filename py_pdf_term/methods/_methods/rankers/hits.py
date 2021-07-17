from math import sqrt
from dataclasses import dataclass
from typing import Dict

from .base import BaseSingleDomainRanker
from ..rankingdata import HITSRankingData
from ..data import MethodTermRanking
from py_pdf_term.candidates import DomainCandidateTermList
from py_pdf_term.tokenizer import Morpheme
from py_pdf_term.tokenizer.langs import (
    JapaneseMorphemeClassifier,
    EnglishMorphemeClassifier,
)
from py_pdf_term._common.data import Term, ScoredTerm
from py_pdf_term._common.extended_math import extended_log10


@dataclass(frozen=True)
class HITSAuthHubData:
    morpheme_auth: Dict[str, float]
    # auth value of the morpheme
    # the more morphemes links to, the larger the auth value becomes
    # initial auth value is 1.0
    morpheme_hub: Dict[str, float]
    # hub value of the term
    # the more morphemes is linked from, the larger the hub value becomes
    # initial hub value is 1.0


class HITSRanker(BaseSingleDomainRanker[HITSRankingData]):
    def __init__(self, threshold: float = 1e-8, max_loop: int = 1000) -> None:
        self._threshold = threshold
        self._max_loop = max_loop
        self._ja_classifier = JapaneseMorphemeClassifier()
        self._en_classifier = EnglishMorphemeClassifier()

    def rank_terms(
        self, domain_candidates: DomainCandidateTermList, ranking_data: HITSRankingData
    ) -> MethodTermRanking:
        auth_hub_data = self._create_auth_hub_data(ranking_data)
        domain_candidates_dict = domain_candidates.to_nostyle_candidates_dict(
            to_str=lambda candidate: candidate.lemma()
        )
        ranking = list(
            map(
                lambda candidate: self._calculate_score(
                    candidate, ranking_data, auth_hub_data
                ),
                domain_candidates_dict.values(),
            )
        )
        ranking.sort(key=lambda term: -term.score)
        return MethodTermRanking(domain_candidates.domain, ranking)

    def _create_auth_hub_data(self, ranking_data: HITSRankingData) -> HITSAuthHubData:
        morpheme_auth: Dict[str, float] = {
            morpheme_lemma: 1.0 for morpheme_lemma in ranking_data.left_freq
        }
        morpheme_hub: Dict[str, float] = {
            morpheme_lemma: 1.0 for morpheme_lemma in ranking_data.right_freq
        }

        converged = False
        loop = 0
        while not converged and loop < self._max_loop:
            new_morpheme_auth = {
                morpheme: sum(map(lambda hub: morpheme_hub[hub], left.keys()), 0.0)
                for morpheme, left in ranking_data.left_freq.items()
            }
            auth_norm = sqrt(sum(map(lambda x: x * x, new_morpheme_auth.values())))
            new_morpheme_auth = {
                morpheme: auth_score / auth_norm
                for morpheme, auth_score in new_morpheme_auth.items()
            }

            new_morpheme_hub = {
                morpheme: sum(map(lambda auth: morpheme_auth[auth], right.keys()), 0.0)
                for morpheme, right in ranking_data.right_freq.items()
            }
            hub_norm = sqrt(sum(map(lambda x: x * x, new_morpheme_hub.values())))
            new_morpheme_hub = {
                morpheme: hub_score / hub_norm
                for morpheme, hub_score in new_morpheme_hub.items()
            }

            converged = all(
                [
                    abs(new_morpheme_auth[morpheme] - morpheme_auth[morpheme])
                    < self._threshold
                    for morpheme in ranking_data.left_freq
                ]
                + [
                    abs(new_morpheme_hub[morpheme] - morpheme_hub[morpheme])
                    < self._threshold
                    for morpheme in ranking_data.right_freq
                ]
            )

            morpheme_auth = new_morpheme_auth
            morpheme_hub = new_morpheme_hub

            loop += 1

        return HITSAuthHubData(morpheme_auth, morpheme_hub)

    def _calculate_score(
        self,
        candidate: Term,
        ranking_data: HITSRankingData,
        auth_hub_data: HITSAuthHubData,
    ) -> ScoredTerm:
        candidate_lemma = candidate.lemma()
        num_morphemes = len(candidate.morphemes)
        num_meaningless_morphemes = sum(
            map(
                lambda morpheme: 1 if self._is_meaningless_morpheme(morpheme) else 0,
                candidate.morphemes,
            )
        )

        if num_morphemes == 0:
            return ScoredTerm(candidate_lemma, 0.0)

        term_freq_score = extended_log10(ranking_data.term_freq.get(candidate_lemma, 0))

        if num_morphemes == 1:
            morpheme_lemma = candidate.morphemes[0].lemma
            auth_hub_score = 0.5 * (
                extended_log10(auth_hub_data.morpheme_hub.get(morpheme_lemma, 0.0))
                + extended_log10(auth_hub_data.morpheme_auth.get(morpheme_lemma, 0.0))
            )
            score = term_freq_score + auth_hub_score
            return ScoredTerm(candidate_lemma, score)

        auth_hub_score = 0.0
        for i, morpheme in enumerate(candidate.morphemes):
            if self._is_meaningless_morpheme(morpheme):
                continue

            if i == 0:
                auth_hub_score += extended_log10(
                    auth_hub_data.morpheme_hub.get(morpheme.lemma, 0.0)
                )
            elif i == num_morphemes - 1:
                auth_hub_score += extended_log10(
                    auth_hub_data.morpheme_auth.get(morpheme.lemma, 0.0)
                )
            else:
                auth_hub_score += extended_log10(
                    auth_hub_data.morpheme_hub.get(morpheme.lemma, 0.0)
                )
                auth_hub_score += extended_log10(
                    auth_hub_data.morpheme_auth.get(morpheme.lemma, 0.0)
                )
                auth_hub_score = auth_hub_score / 2

        auth_hub_score /= num_morphemes - num_meaningless_morphemes

        score = term_freq_score + auth_hub_score
        return ScoredTerm(candidate_lemma, score)

    def _is_meaningless_morpheme(self, morpheme: Morpheme) -> bool:
        is_ja_meaningless = self._ja_classifier.is_meaningless(morpheme)
        is_en_meaningless = self._en_classifier.is_meaningless(morpheme)
        return is_ja_meaningless or is_en_meaningless
