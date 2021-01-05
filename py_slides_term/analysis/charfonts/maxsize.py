from dataclasses import dataclass
from typing import Dict

from ..share import AnalysisRunner
from py_slides_term.candidates import DomainCandidateTermList
from py_slides_term.share.data import Term


@dataclass(frozen=True)
class DomainTermMaxsize:
    domain: str
    # unique domain name
    term_maxsize: Dict[str, float]
    # max fontsize of the term in the domain
    # default of this is zero


class TermMaxsizeAnalyzer:
    # public
    def __init__(self, ignore_augmented: bool = True):
        self._runner = AnalysisRunner(ignore_augmented=ignore_augmented)

    def analyze(self, domain_candidates: DomainCandidateTermList) -> DomainTermMaxsize:
        domain_candidates_set = domain_candidates.to_domain_candidate_term_set()

        def update(
            term_maxsize: DomainTermMaxsize,
            pdf_id: int,
            page_num: int,
            subcandidate: Term,
        ):
            subcandidate_str = str(subcandidate)
            if subcandidate_str not in domain_candidates_set.candidates:
                return

            term_maxsize.term_maxsize[subcandidate_str] = max(
                term_maxsize.term_maxsize.get(subcandidate_str, 0),
                subcandidate.fontsize,
            )

        term_maxsize = self._runner.run_through_subcandidates(
            domain_candidates,
            DomainTermMaxsize(domain_candidates.domain, dict()),
            update,
        )
        return term_maxsize
