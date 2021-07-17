from dataclasses import dataclass
from typing import Dict

from ..runner import AnalysisRunner
from py_pdf_term.candidates import DomainCandidateTermList
from py_pdf_term.tokenizer import Morpheme
from py_pdf_term.tokenizer.langs import (
    JapaneseMorphemeClassifier,
    EnglishMorphemeClassifier,
)
from py_pdf_term._common.data import Term


@dataclass(frozen=True)
class DomainLeftRightFrequency:
    domain: str
    # unique domain name
    left_freq: Dict[str, Dict[str, int]]
    # number of occurrences of lemmatized (left, morpheme) in the domain
    # if morpheme or left is meaningless, this is fixed at zero
    right_freq: Dict[str, Dict[str, int]]
    # number of occurrences of lemmatized (morpheme, right) in the domain
    # if morpheme or right is meaningless, this is fixed at zero


class TermLeftRightFrequencyAnalyzer:
    def __init__(self, ignore_augmented: bool = True) -> None:
        self._ignore_augmented = ignore_augmented
        self._ja_classifier = JapaneseMorphemeClassifier()
        self._en_classifier = EnglishMorphemeClassifier()
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
            num_morphemes = len(candidate.morphemes)
            for i in range(num_morphemes):
                morpheme = candidate.morphemes[i]
                if self._is_meaningless_morpheme(morpheme):
                    lrfreq.left_freq[morpheme.lemma] = dict()
                    lrfreq.right_freq[morpheme.lemma] = dict()
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
        morpheme = candidate.morphemes[idx]

        if idx == 0:
            left = lrfreq.left_freq.get(morpheme.lemma, dict())
            lrfreq.left_freq[morpheme.lemma] = left
            return

        left_morpheme = candidate.morphemes[idx - 1]
        if not self._is_meaningless_morpheme(left_morpheme):
            left = lrfreq.left_freq.get(morpheme.lemma, dict())
            left[left_morpheme.lemma] = left.get(left_morpheme.lemma, 0) + 1
            lrfreq.left_freq[morpheme.lemma] = left
        else:
            left = lrfreq.left_freq.get(morpheme.lemma, dict())
            lrfreq.left_freq[morpheme.lemma] = left

    def _update_right_freq(
        self, lrfreq: DomainLeftRightFrequency, candidate: Term, idx: int
    ) -> None:
        num_morphemes = len(candidate.morphemes)
        morpheme = candidate.morphemes[idx]

        if idx == num_morphemes - 1:
            right = lrfreq.right_freq.get(morpheme.lemma, dict())
            lrfreq.right_freq[morpheme.lemma] = right
            return

        right_morpheme = candidate.morphemes[idx + 1]
        if not self._is_meaningless_morpheme(right_morpheme):
            right = lrfreq.right_freq.get(morpheme.lemma, dict())
            right[right_morpheme.lemma] = right.get(right_morpheme.lemma, 0) + 1
            lrfreq.right_freq[morpheme.lemma] = right
        else:
            right = lrfreq.right_freq.get(morpheme.lemma, dict())
            lrfreq.right_freq[morpheme.lemma] = right

    def _is_meaningless_morpheme(self, morpheme: Morpheme) -> bool:
        is_ja_meaningless = self._ja_classifier.is_meaningless(morpheme)
        is_en_meaningless = self._en_classifier.is_meaningless(morpheme)
        return is_ja_meaningless or is_en_meaningless
