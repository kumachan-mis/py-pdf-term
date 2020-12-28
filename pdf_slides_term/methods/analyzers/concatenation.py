from dataclasses import dataclass
from typing import Dict

from pdf_slides_term.candidates.data import DomainCandidateTermList
from pdf_slides_term.mecab.filter import MeCabMorphemeFilter
from pdf_slides_term.share.data import TechnicalTerm


@dataclass
class TermConcatenation:
    left_freq: Dict[str, Dict[str, int]]
    # number of occurrences of (left, morpheme)
    # if morpheme or left is a modifying particle, this is fixed at zero
    right_freq: Dict[str, Dict[str, int]]
    # number of occurrences of (morpheme, right)
    # if morpheme or right is a modifying particle, this is fixed at zero


class TermConcatenationAnalyzer:
    # public
    def __init__(self, ignore_augmented=True):
        self._morpheme_filter = MeCabMorphemeFilter()
        self._ignore_augmented = ignore_augmented

    def analyze(self, domain_candidates: DomainCandidateTermList) -> TermConcatenation:
        term_concat = TermConcatenation(dict(), dict())

        for xml_candidates in domain_candidates.xmls:
            for page_candidates in xml_candidates.pages:
                for candidate in page_candidates.candidates:
                    if self._ignore_augmented and candidate.augmented:
                        continue
                    self._update_concat(term_concat, candidate)

        return term_concat

    # private
    def _update_concat(self, term_concat: TermConcatenation, candidate: TechnicalTerm):
        num_morphemes = len(candidate.morphemes)
        for i in range(num_morphemes):
            morpheme = candidate.morphemes[i]
            morpheme_str = str(morpheme)
            if self._morpheme_filter.is_modifying_particle(morpheme):
                continue

            if i > 0:
                left_morpheme = candidate.morphemes[i - 1]
                left_morpheme_str = str(left_morpheme)

                if not self._morpheme_filter.is_modifying_particle(left_morpheme):
                    left = term_concat.left_freq.get(morpheme_str, dict())
                    left[left_morpheme_str] = left.get(left_morpheme_str, 0) + 1
                    term_concat.left_freq[morpheme_str] = left

                    right = term_concat.right_freq.get(left_morpheme_str, dict())
                    right[morpheme_str] = right.get(morpheme_str, 0) + 1
                    term_concat.right_freq[left_morpheme_str] = right

            if i < num_morphemes - 1:
                right_morpheme = candidate.morphemes[i + 1]
                right_morpheme_str = str(right_morpheme)

                if not self._morpheme_filter.is_modifying_particle(right_morpheme):
                    right = term_concat.right_freq.get(morpheme_str, dict())
                    right[right_morpheme_str] = right.get(right_morpheme_str, 0) + 1
                    term_concat.right_freq[morpheme_str] = right

                    left = term_concat.left_freq.get(right_morpheme_str, dict())
                    left[morpheme_str] = right.get(morpheme_str, 0) + 1
                    term_concat.left_freq[right_morpheme_str] = left
