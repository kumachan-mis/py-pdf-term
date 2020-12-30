from dataclasses import dataclass
from typing import Dict

from pdf_slides_term.candidates.data import DomainCandidateTermList
from pdf_slides_term.share.data import TechnicalTerm


@dataclass(frozen=True)
class TermCharFont:
    term_maxsize: Dict[str, float]
    # max fontsize of the term in the domain
    # default of this is zero


class TermCharFontAnalyzer:
    # public
    def __init__(self, ignore_augmented: bool = True):
        self._ignore_augmented = ignore_augmented

    def analyze(self, domain_candidates: DomainCandidateTermList) -> TermCharFont:
        return TermCharFont(self.analyze_term_maxsize(domain_candidates))

    def analyze_term_maxsize(
        self, domain_candidates: DomainCandidateTermList
    ) -> Dict[str, float]:
        term_maxsize: Dict[str, float] = dict()

        for xml_candidates in domain_candidates.xmls:
            for page_candidates in xml_candidates.pages:
                for candidate in page_candidates.candidates:
                    if self._ignore_augmented and candidate.augmented:
                        continue
                    self._update_term_maxsize(term_maxsize, candidate)

        return term_maxsize

    # private
    def _update_term_maxsize(
        self,
        term_maxsize: Dict[str, float],
        candidate: TechnicalTerm,
    ):
        num_morphemes = len(candidate.morphemes)
        for i in range(num_morphemes):
            for j in range(i + 1, num_morphemes + 1):
                sub_morphemes = candidate.morphemes[i:j]
                sub_candidate = TechnicalTerm(sub_morphemes, candidate.fontsize, True)
                sub_candidate_str = str(sub_candidate)
                term_maxsize[sub_candidate_str] = max(
                    term_maxsize.get(sub_candidate_str, 0),
                    sub_candidate.fontsize,
                )
