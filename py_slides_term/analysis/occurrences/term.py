from dataclasses import dataclass
from typing import Set, Dict

from ..share import AnalysisRunner
from py_slides_term.candidates import DomainCandidateTermList
from py_slides_term.share.data import Term


@dataclass(frozen=True)
class DomainTermOccurrence:
    domain: str
    # unique domain name
    term_freq: Dict[str, int]
    # brute force counting of term occurrences in the domain
    # count even if the term occurs as a part of a phrase
    doc_term_freq: Dict[str, int]
    # number of documents in the domain that contain the term
    # count even if the term occurs as a part of a phrase


@dataclass(frozen=True)
class _DomainTermOccurrence:
    domain: str
    # unique domain name
    term_freq: Dict[str, int]
    # brute force counting of term occurrences in the domain
    # count even if the term occurs as a part of a phrase
    doc_term_set: Dict[str, Set[int]]
    # set of document IDs in the domain that contain the term
    # add even if the term occurs as a part of a phrase


class TermOccurrenceAnalyzer:
    # public
    def __init__(self, ignore_augmented: bool = True):
        self._runner = AnalysisRunner(ignore_augmented=ignore_augmented)

    def analyze(
        self, domain_candidates: DomainCandidateTermList
    ) -> DomainTermOccurrence:
        domain_candidates_set = domain_candidates.to_term_str_set()

        def update(
            term_occ: _DomainTermOccurrence,
            pdf_id: int,
            page_num: int,
            subcandidate: Term,
        ):
            subcandidate_str = str(subcandidate)
            if subcandidate_str not in domain_candidates_set:
                return
            term_occ.term_freq[subcandidate_str] = (
                term_occ.term_freq.get(subcandidate_str, 0) + 1
            )
            doc_term_set = term_occ.doc_term_set.get(subcandidate_str, set())
            doc_term_set.add(pdf_id)
            term_occ.doc_term_set[subcandidate_str] = doc_term_set

        term_occ = self._runner.run_through_subcandidates(
            domain_candidates,
            _DomainTermOccurrence(domain_candidates.domain, dict(), dict()),
            update,
        )
        term_occ = self._finalize(term_occ)
        return term_occ

    # private
    def _finalize(self, term_occ: _DomainTermOccurrence) -> DomainTermOccurrence:
        doc_term_freq = {
            candidate_str: len(doc_term_set)
            for candidate_str, doc_term_set in term_occ.doc_term_set.items()
        }
        return DomainTermOccurrence(term_occ.domain, term_occ.term_freq, doc_term_freq)
