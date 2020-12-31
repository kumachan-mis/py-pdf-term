from dataclasses import dataclass
from typing import Dict

from pdf_slides_term.analysis.runner import AnalysisRunner
from pdf_slides_term.candidates.data import DomainCandidateTermList
from pdf_slides_term.share.data import TechnicalTerm


@dataclass(frozen=True)
class TermCooccurrence:
    container_term_freqs: Dict[str, Dict[str, int]]
    # brute force counting of occurrences of (term, container) in the domain
    # (term, container) is valid iff the container contains the term as a subsequence


class TermCooccurrenceAnalyzer:
    # public
    def __init__(self, ignore_augmented: bool = True):
        self._runner = AnalysisRunner(ignore_augmented=ignore_augmented)

    def analyze(self, domain_candidates: DomainCandidateTermList) -> TermCooccurrence:
        return TermCooccurrence(self.analyze_container_term_freqs(domain_candidates))

    def analyze_container_term_freqs(
        self, domain_candidates: DomainCandidateTermList
    ) -> Dict[str, Dict[str, int]]:
        domain_candidates_set = domain_candidates.to_domain_candidate_term_set()

        def update(
            container_term_freqs: Dict[str, Dict[str, int]],
            xml_id: int,
            page_num: int,
            candidate: TechnicalTerm,
        ):
            candidate_str = str(candidate)
            num_morphemes = len(candidate.morphemes)
            for i in range(num_morphemes):
                for j in range(i + 1, num_morphemes + 1):
                    sub_candidate = TechnicalTerm(
                        candidate.morphemes[i:j],
                        candidate.fontsize,
                        candidate.augmented,
                    )
                    sub_candidate_str = str(sub_candidate)
                    if sub_candidate_str not in domain_candidates_set.candidates:
                        return

                    container_term_freq = container_term_freqs.get(
                        sub_candidate_str, dict()
                    )
                    container_term_freq[candidate_str] = (
                        container_term_freq.get(candidate_str, 0) + 1
                    )
                    container_term_freqs[sub_candidate_str] = container_term_freq

        container_term_freqs = self._runner.run_through_candidates(
            domain_candidates, dict(), update
        )
        return container_term_freqs
