from dataclasses import dataclass
from typing import Dict

from py_pdf_term._common.data import Term
from py_pdf_term.candidates import DomainCandidateTermList
from py_pdf_term.tokenizer import Token
from py_pdf_term.tokenizer.langs import EnglishTokenClassifier, JapaneseTokenClassifier

from ..runner import AnalysisRunner


@dataclass(frozen=True)
class DomainLeftRightFrequency:
    domain: str
    # unique domain name
    left_freq: Dict[str, Dict[str, int]]
    # number of occurrences of lemmatized (left, token) in the domain
    # if token or left is meaningless, this is fixed at zero
    right_freq: Dict[str, Dict[str, int]]
    # number of occurrences of lemmatized (token, right) in the domain
    # if token or right is meaningless, this is fixed at zero


class TermLeftRightFrequencyAnalyzer:
    def __init__(self, ignore_augmented: bool = True) -> None:
        self._ignore_augmented = ignore_augmented
        self._ja_classifier = JapaneseTokenClassifier()
        self._en_classifier = EnglishTokenClassifier()
        self._runner = AnalysisRunner(ignore_augmented=ignore_augmented)

    def analyze(
        self, domain_candidates: DomainCandidateTermList
    ) -> DomainLeftRightFrequency:
        def update(
            lrfreq: DomainLeftRightFrequency,
            pdf_id: int,
            page_num: int,
            candidate: Term,
        ) -> None:
            num_tokens = len(candidate.tokens)
            for i in range(num_tokens):
                token = candidate.tokens[i]
                if self._is_meaningless_token(token):
                    lrfreq.left_freq[token.lemma] = dict()
                    lrfreq.right_freq[token.lemma] = dict()
                    continue

                self._update_left_freq(lrfreq, candidate, i)
                self._update_right_freq(lrfreq, candidate, i)

        lrfreq = self._runner.run_through_candidates(
            domain_candidates,
            DomainLeftRightFrequency(domain_candidates.domain, dict(), dict()),
            update,
        )

        return lrfreq

    def _update_left_freq(
        self, lrfreq: DomainLeftRightFrequency, candidate: Term, idx: int
    ) -> None:
        token = candidate.tokens[idx]

        if idx == 0:
            left = lrfreq.left_freq.get(token.lemma, dict())
            lrfreq.left_freq[token.lemma] = left
            return

        left_token = candidate.tokens[idx - 1]
        if not self._is_meaningless_token(left_token):
            left = lrfreq.left_freq.get(token.lemma, dict())
            left[left_token.lemma] = left.get(left_token.lemma, 0) + 1
            lrfreq.left_freq[token.lemma] = left
        else:
            left = lrfreq.left_freq.get(token.lemma, dict())
            lrfreq.left_freq[token.lemma] = left

    def _update_right_freq(
        self, lrfreq: DomainLeftRightFrequency, candidate: Term, idx: int
    ) -> None:
        num_tokens = len(candidate.tokens)
        token = candidate.tokens[idx]

        if idx == num_tokens - 1:
            right = lrfreq.right_freq.get(token.lemma, dict())
            lrfreq.right_freq[token.lemma] = right
            return

        right_token = candidate.tokens[idx + 1]
        if not self._is_meaningless_token(right_token):
            right = lrfreq.right_freq.get(token.lemma, dict())
            right[right_token.lemma] = right.get(right_token.lemma, 0) + 1
            lrfreq.right_freq[token.lemma] = right
        else:
            right = lrfreq.right_freq.get(token.lemma, dict())
            lrfreq.right_freq[token.lemma] = right

    def _is_meaningless_token(self, token: Token) -> bool:
        is_ja_meaningless = self._ja_classifier.is_meaningless(token)
        is_en_meaningless = self._en_classifier.is_meaningless(token)
        return is_ja_meaningless or is_en_meaningless
