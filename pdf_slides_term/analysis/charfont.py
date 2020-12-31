from dataclasses import dataclass
from typing import Dict

from pdf_slides_term.analysis.runner import AnalysisRunner
from pdf_slides_term.candidates.data import DomainCandidateTermList
from pdf_slides_term.share.data import Term


@dataclass(frozen=True)
class TermCharFont:
    term_maxsize: Dict[str, float]
    # max fontsize of the term in the domain
    # default of this is zero


class TermCharFontAnalyzer:
    # public
    def __init__(self, ignore_augmented: bool = True):
        self._runner = AnalysisRunner(ignore_augmented=ignore_augmented)

    def analyze(self, domain_candidates: DomainCandidateTermList) -> TermCharFont:
        return TermCharFont(self.analyze_term_maxsize(domain_candidates))

    def analyze_term_maxsize(
        self, domain_candidates: DomainCandidateTermList
    ) -> Dict[str, float]:
        domain_candidates_set = domain_candidates.to_domain_candidate_term_set()

        def update(
            term_maxsize: Dict[str, float],
            xml_id: int,
            page_num: int,
            subcandidate: Term,
        ):
            subcandidate_str = str(subcandidate)
            if subcandidate_str not in domain_candidates_set.candidates:
                return

            term_maxsize[subcandidate_str] = max(
                term_maxsize.get(subcandidate_str, 0), subcandidate.fontsize
            )

        term_maxsize = self._runner.run_through_subcandidates(
            domain_candidates, dict(), update
        )
        return term_maxsize
