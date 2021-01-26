from dataclasses import dataclass
from typing import Dict

from ..share import AnalysisRunner
from py_slides_term.candidates import DomainCandidateTermList
from py_slides_term.morphemes import JapaneseMorphemeClassifier, BaseMorpheme
from py_slides_term.share.data import Term


@dataclass(frozen=True)
class DomainLeftRightFrequency:
    domain: str
    # unique domain name
    left_freq: Dict[str, Dict[str, int]]
    # number of occurrences of (left, morpheme) in the domain
    # if morpheme or left is meaningless (a modifying particle or a symbol),
    # this is fixed at zero
    right_freq: Dict[str, Dict[str, int]]
    # number of occurrences of (morpheme, right) in the domain
    # if morpheme or right is meaningless (a modifying particle or a symbol),
    # this is fixed at zero


class TermLeftRightFrequencyAnalyzer:
    # public
    def __init__(self, ignore_augmented: bool = True):
        self._ignore_augmented = ignore_augmented
        self._classifier = JapaneseMorphemeClassifier()
        self._runner = AnalysisRunner(ignore_augmented=ignore_augmented)

    def analyze(
        self, domain_candidates: DomainCandidateTermList
    ) -> DomainLeftRightFrequency:
        def update(
            lrfreq: DomainLeftRightFrequency,
            pdf_id: int,
            page_num: int,
            candidate: Term,
        ):
            num_morphemes = len(candidate.morphemes)
            for i in range(num_morphemes):
                morpheme = candidate.morphemes[i]
                morpheme_str = str(morpheme)
                if self._is_meaningless_morpheme(morpheme):
                    lrfreq.left_freq[morpheme_str] = dict()
                    lrfreq.right_freq[morpheme_str] = dict()
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
    ):
        morpheme = candidate.morphemes[idx]
        morpheme_str = str(morpheme)

        if idx == 0:
            left = lrfreq.left_freq.get(morpheme_str, dict())
            lrfreq.left_freq[morpheme_str] = left
            return

        left_morpheme = candidate.morphemes[idx - 1]
        left_morpheme_str = str(left_morpheme)

        if not self._is_meaningless_morpheme(left_morpheme):
            left = lrfreq.left_freq.get(morpheme_str, dict())
            left[left_morpheme_str] = left.get(left_morpheme_str, 0) + 1
            lrfreq.left_freq[morpheme_str] = left

            right = lrfreq.right_freq.get(left_morpheme_str, dict())
            right[morpheme_str] = right.get(morpheme_str, 0) + 1
            lrfreq.right_freq[left_morpheme_str] = right
        else:
            left = lrfreq.left_freq.get(morpheme_str, dict())
            lrfreq.left_freq[morpheme_str] = left

    def _update_right_freq(
        self, lrfreq: DomainLeftRightFrequency, candidate: Term, idx: int
    ):
        num_morphemes = len(candidate.morphemes)
        morpheme = candidate.morphemes[idx]
        morpheme_str = str(morpheme)

        if idx == num_morphemes - 1:
            right = lrfreq.right_freq.get(morpheme_str, dict())
            lrfreq.right_freq[morpheme_str] = right
            return

        right_morpheme = candidate.morphemes[idx + 1]
        right_morpheme_str = str(right_morpheme)

        if not self._is_meaningless_morpheme(right_morpheme):
            right = lrfreq.right_freq.get(morpheme_str, dict())
            right[right_morpheme_str] = right.get(right_morpheme_str, 0) + 1
            lrfreq.right_freq[morpheme_str] = right

            left = lrfreq.left_freq.get(right_morpheme_str, dict())
            left[morpheme_str] = right.get(morpheme_str, 0) + 1
            lrfreq.left_freq[right_morpheme_str] = left
        else:
            right = lrfreq.right_freq.get(morpheme_str, dict())
            lrfreq.right_freq[morpheme_str] = right

    def _is_meaningless_morpheme(self, morpheme: BaseMorpheme) -> bool:
        is_modifying_particle = self._classifier.is_modifying_particle(morpheme)
        is_connector_punct = self._classifier.is_connector_punct(morpheme)
        return is_modifying_particle or is_connector_punct
