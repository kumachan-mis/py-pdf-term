from math import sqrt, log10
from dataclasses import dataclass
from py_slides_term.morphemes.classifier import EnglishMorphemeClassifier
from typing import Dict

from .base import BaseSingleDomainRanker
from ..rankingdata import HITSRankingData
from ..data import DomainTermRanking, ScoredTerm
from py_slides_term.candidates import DomainCandidateTermList
from py_slides_term.morphemes import JapaneseMorphemeClassifier, BaseMorpheme
from py_slides_term.share.data import Term


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
    # public
    def __init__(self, threshold: float = 1e-8):
        self._threshold = threshold
        self._ja_classifier = JapaneseMorphemeClassifier()
        self._en_classifier = EnglishMorphemeClassifier()

    def rank_terms(
        self, domain_candidates: DomainCandidateTermList, ranking_data: HITSRankingData
    ) -> DomainTermRanking:
        auth_hub_data = self._create_auth_hub_data(ranking_data)
        domain_candidates_dict = domain_candidates.to_domain_candidate_term_dict()
        ranking = list(
            map(
                lambda candidate: self._calculate_score(
                    candidate, ranking_data, auth_hub_data
                ),
                domain_candidates_dict.candidates.values(),
            )
        )
        ranking.sort(key=lambda term: -term.score)
        return DomainTermRanking(domain_candidates.domain, ranking)

    # private
    def _create_auth_hub_data(self, ranking_data: HITSRankingData) -> HITSAuthHubData:
        morpheme_auth: Dict[str, float] = {
            morpheme: 1.0 for morpheme in ranking_data.left_freq
        }
        morpheme_hub: Dict[str, float] = {
            morpheme: 1.0 for morpheme in ranking_data.right_freq
        }

        converged = False
        while not converged:
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

        return HITSAuthHubData(morpheme_auth, morpheme_hub)

    def _calculate_score(
        self,
        candidate: Term,
        ranking_data: HITSRankingData,
        auth_hub_data: HITSAuthHubData,
    ) -> ScoredTerm:
        candidate_str = str(candidate)
        num_morphemes = len(candidate.morphemes)
        num_meaningless_morphemes = sum(
            map(
                lambda morpheme: 1 if self._is_meaningless_morpheme(morpheme) else 0,
                candidate.morphemes,
            )
        )

        if num_morphemes == 0:
            return ScoredTerm(candidate_str, 0.0)

        term_maxsize_score = (
            log10(ranking_data.term_maxsize[candidate_str])
            if ranking_data.term_maxsize is not None
            else 0.0
        )
        term_freq_score = log10(ranking_data.term_freq[candidate_str])

        if num_morphemes == 1:
            morpheme_str = str(candidate.morphemes[0])
            auth_hub_score = 0.5 * (
                log10(auth_hub_data.morpheme_hub[morpheme_str] + 1.0)
                + log10(auth_hub_data.morpheme_auth[morpheme_str] + 1.0)
            )
            score = term_maxsize_score + term_freq_score + auth_hub_score
            return ScoredTerm(candidate_str, score)

        auth_hub_score = 0.0
        for i, morpheme in enumerate(candidate.morphemes):
            if self._is_meaningless_morpheme(morpheme):
                continue

            morpheme_str = str(morpheme)
            if i == 0:
                auth_hub_score += log10(auth_hub_data.morpheme_hub[morpheme_str] + 1.0)
            elif i == num_morphemes - 1:
                auth_hub_score += log10(auth_hub_data.morpheme_auth[morpheme_str] + 1.0)
            else:
                auth_hub_score += 0.5 * (
                    log10(auth_hub_data.morpheme_hub[morpheme_str] + 1.0)
                    + log10(auth_hub_data.morpheme_auth[morpheme_str] + 1.0)
                )

        auth_hub_score /= num_morphemes - num_meaningless_morphemes

        score = term_maxsize_score + term_freq_score + auth_hub_score
        return ScoredTerm(candidate_str, score)

    def _is_meaningless_morpheme(self, morpheme: BaseMorpheme) -> bool:
        is_modifying_particle = self._ja_classifier.is_modifying_particle(morpheme)
        is_ja_connector_symbol = self._ja_classifier.is_connector_symbol(morpheme)
        is_en_connector_symbol = self._en_classifier.is_connector_symbol(morpheme)
        return is_modifying_particle or is_ja_connector_symbol or is_en_connector_symbol
