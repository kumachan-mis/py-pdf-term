from dataclasses import dataclass
from math import sqrt
from typing import Dict

from py_pdf_term._common.data import ScoredTerm, Term
from py_pdf_term._common.extended_math import extended_log10
from py_pdf_term.candidates import DomainCandidateTermList
from py_pdf_term.tokenizer import Token
from py_pdf_term.tokenizer.langs import EnglishTokenClassifier, JapaneseTokenClassifier

from ..data import MethodTermRanking
from ..rankingdata import HITSRankingData
from .base import BaseSingleDomainRanker


@dataclass(frozen=True)
class HITSAuthHubData:
    token_auth: Dict[str, float]
    # auth value of the token
    # the more tokens links to, the larger the auth value becomes
    # initial auth value is 1.0
    token_hub: Dict[str, float]
    # hub value of the term
    # the more tokens is linked from, the larger the hub value becomes
    # initial hub value is 1.0


class HITSRanker(BaseSingleDomainRanker[HITSRankingData]):
    def __init__(self, threshold: float = 1e-8, max_loop: int = 1000) -> None:
        self._threshold = threshold
        self._max_loop = max_loop
        self._ja_classifier = JapaneseTokenClassifier()
        self._en_classifier = EnglishTokenClassifier()

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
        token_auth: Dict[str, float] = {
            token_lemma: 1.0 for token_lemma in ranking_data.left_freq
        }
        token_hub: Dict[str, float] = {
            token_lemma: 1.0 for token_lemma in ranking_data.right_freq
        }

        converged = False
        loop = 0
        while not converged and loop < self._max_loop:
            new_token_auth = {
                token: sum(map(lambda hub: token_hub[hub], left.keys()), 0.0)
                for token, left in ranking_data.left_freq.items()
            }
            auth_norm = sqrt(sum(map(lambda x: x * x, new_token_auth.values())))
            new_token_auth = {
                token: auth_score / auth_norm
                for token, auth_score in new_token_auth.items()
            }

            new_token_hub = {
                token: sum(map(lambda auth: token_auth[auth], right.keys()), 0.0)
                for token, right in ranking_data.right_freq.items()
            }
            hub_norm = sqrt(sum(map(lambda x: x * x, new_token_hub.values())))
            new_token_hub = {
                token: hub_score / hub_norm
                for token, hub_score in new_token_hub.items()
            }

            converged = all(
                [
                    abs(new_token_auth[token] - token_auth[token]) < self._threshold
                    for token in ranking_data.left_freq
                ]
                + [
                    abs(new_token_hub[token] - token_hub[token]) < self._threshold
                    for token in ranking_data.right_freq
                ]
            )

            token_auth = new_token_auth
            token_hub = new_token_hub

            loop += 1

        return HITSAuthHubData(token_auth, token_hub)

    def _calculate_score(
        self,
        candidate: Term,
        ranking_data: HITSRankingData,
        auth_hub_data: HITSAuthHubData,
    ) -> ScoredTerm:
        candidate_lemma = candidate.lemma()
        num_tokens = len(candidate.tokens)
        num_meaningless_tokens = sum(
            map(
                lambda token: 1 if self._is_meaningless_token(token) else 0,
                candidate.tokens,
            )
        )

        if num_tokens == 0:
            return ScoredTerm(candidate_lemma, 0.0)

        term_freq_score = extended_log10(ranking_data.term_freq.get(candidate_lemma, 0))

        if num_tokens == 1:
            token_lemma = candidate.tokens[0].lemma
            auth_hub_score = 0.5 * (
                extended_log10(auth_hub_data.token_hub.get(token_lemma, 0.0))
                + extended_log10(auth_hub_data.token_auth.get(token_lemma, 0.0))
            )
            score = term_freq_score + auth_hub_score
            return ScoredTerm(candidate_lemma, score)

        auth_hub_score = 0.0
        for i, token in enumerate(candidate.tokens):
            if self._is_meaningless_token(token):
                continue

            if i == 0:
                auth_hub_score += extended_log10(
                    auth_hub_data.token_hub.get(token.lemma, 0.0)
                )
            elif i == num_tokens - 1:
                auth_hub_score += extended_log10(
                    auth_hub_data.token_auth.get(token.lemma, 0.0)
                )
            else:
                auth_hub_score += extended_log10(
                    auth_hub_data.token_hub.get(token.lemma, 0.0)
                )
                auth_hub_score += extended_log10(
                    auth_hub_data.token_auth.get(token.lemma, 0.0)
                )
                auth_hub_score = auth_hub_score / 2

        auth_hub_score /= num_tokens - num_meaningless_tokens

        score = term_freq_score + auth_hub_score
        return ScoredTerm(candidate_lemma, score)

    def _is_meaningless_token(self, token: Token) -> bool:
        is_ja_meaningless = self._ja_classifier.is_meaningless(token)
        is_en_meaningless = self._en_classifier.is_meaningless(token)
        return is_ja_meaningless or is_en_meaningless
