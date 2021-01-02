from dataclasses import dataclass
from typing import Set, Dict

from .runner import AnalysisRunner
from py_slides_term.candidates import DomainCandidateTermList
from py_slides_term.share.data import Term


@dataclass(frozen=True)
class TermCooccurrence:
    container_terms: Dict[str, Set[str]]
    # set of containers of the term in the domain
    # (term, container) is valid iff the container contains the term
    # as a proper subsequence


class TermCooccurrenceAnalyzer:
    # public
    def __init__(self, ignore_augmented: bool = True):
        self._runner = AnalysisRunner(ignore_augmented=ignore_augmented)

    def analyze(self, domain_candidates: DomainCandidateTermList) -> TermCooccurrence:
        return TermCooccurrence(self.analyze_container_terms(domain_candidates))

    def analyze_container_terms(
        self, domain_candidates: DomainCandidateTermList
    ) -> Dict[str, Set[str]]:
        domain_candidates_set = domain_candidates.to_domain_candidate_term_set()

        def update(
            container_terms: Dict[str, Set[str]],
            pdf_id: int,
            page_num: int,
            candidate: Term,
        ):
            candidate_str = str(candidate)
            container_terms[candidate_str] = container_terms.get(candidate_str, set())

            num_morphemes = len(candidate.morphemes)
            for i in range(num_morphemes):
                jstart, jstop = i + 1, (num_morphemes + 1 if i > 0 else num_morphemes)
                for j in range(jstart, jstop):
                    subcandidate = Term(
                        candidate.morphemes[i:j],
                        candidate.fontsize,
                        candidate.augmented,
                    )
                    subcandidate_str = str(subcandidate)
                    if subcandidate_str not in domain_candidates_set.candidates:
                        continue

                    container_term_set = container_terms.get(subcandidate_str, set())
                    container_term_set.add(candidate_str)
                    container_terms[subcandidate_str] = container_term_set

        container_terms = self._runner.run_through_candidates(
            domain_candidates, dict(), update
        )
        return container_terms
