from dataclasses import dataclass
from typing import Dict

from pdf_slides_term.candidates.data import DomainCandidateTermList
from pdf_slides_term.share.data import TechnicalTerm


@dataclass
class TermOccurrence:
    term_freq: Dict[str, int]
    # brute force counting of term occurrences
    # count even if the term occurs as a part of a phrase


class TermOccurrenceAnalyzer:
    # public
    def __init__(self, ignore_augmented=True):
        self._ignore_augmented = ignore_augmented

    def analyze(self, domain_candidates: DomainCandidateTermList) -> TermOccurrence:
        return TermOccurrence(self.analyze_term_freq(domain_candidates))

    def analyze_term_freq(
        self, domain_candidates: DomainCandidateTermList
    ) -> Dict[str, int]:
        term_freq: Dict[str, int] = dict()

        for xml_candidates in domain_candidates.xmls:
            for page_candidates in xml_candidates.pages:
                for candidate in page_candidates.candidates:
                    if self._ignore_augmented and candidate.augmented:
                        continue
                    self._update_term_freq(term_freq, candidate)

        return term_freq

    # private
    def _update_term_freq(self, term_freq: Dict[str, int], candidate: TechnicalTerm):
        num_morphemes = len(candidate.morphemes)
        for i in range(num_morphemes):
            for j in range(i + 1, num_morphemes + 1):
                sub_morphemes = candidate.morphemes[i:j]
                sub_candidate = TechnicalTerm(sub_morphemes, candidate.fontsize, True)
                sub_candidate_str = str(sub_candidate)
                term_freq[sub_candidate_str] = term_freq.get(sub_candidate_str, 0) + 1
