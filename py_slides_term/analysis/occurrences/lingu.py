from dataclasses import dataclass
from typing import Set, Dict

from ..share import AnalysisRunner
from py_slides_term.candidates import DomainCandidateTermList
from py_slides_term.share.data import Term, LinguSeq


@dataclass(frozen=True)
class DomainLinguOccurrence:
    domain: str
    # unique domain name
    lingu_freq: Dict[LinguSeq, int]
    # brute force counting of linguistic sequence occurrences in the domain
    # count even if the term occurs as a part of a phrase
    doc_lingu_freq: Dict[LinguSeq, int]
    # number of documents in the domain that contain the linguistic sequence
    # count even if the term occurs as a part of a phrase


@dataclass(frozen=True)
class _DomainLinguOccurrence:
    domain: str
    # unique domain name
    lingu_freq: Dict[LinguSeq, int]
    # brute force counting of linguistic sequence occurrences in the domain
    # count even if the term occurs as a part of a phrase
    doc_lingu_set: Dict[LinguSeq, Set[int]]
    # set of document IDs in the domain that contain the linguistic sequence
    # add even if the term occurs as a part of a phrase


class LinguOccurrenceAnalyzer:
    # public
    def __init__(self, ignore_augmented: bool = True):
        self._runner = AnalysisRunner(ignore_augmented=ignore_augmented)

    def analyze(
        self, domain_candidates: DomainCandidateTermList
    ) -> DomainLinguOccurrence:
        domain_candidates_set = domain_candidates.to_domain_candidate_term_set()

        def update(
            lingu_occ: _DomainLinguOccurrence,
            pdf_id: int,
            page_num: int,
            subcandidate: Term,
        ):
            if str(subcandidate) not in domain_candidates_set.candidates:
                return
            sub_lingu_seq = subcandidate.linguistic_sequence()
            lingu_occ.lingu_freq[sub_lingu_seq] = (
                lingu_occ.lingu_freq.get(sub_lingu_seq, 0) + 1
            )
            sub_lingu_seq = subcandidate.linguistic_sequence()
            doc_lingu_set = lingu_occ.doc_lingu_set.get(sub_lingu_seq, set())
            doc_lingu_set.add(pdf_id)
            lingu_occ.doc_lingu_set[sub_lingu_seq] = doc_lingu_set

        lingu_occ = self._runner.run_through_subcandidates(
            domain_candidates,
            _DomainLinguOccurrence(domain_candidates.domain, dict(), dict()),
            update,
        )
        lingu_occ = self._finalize(lingu_occ)
        return lingu_occ

    # private
    def _finalize(self, lingu_occ: _DomainLinguOccurrence) -> DomainLinguOccurrence:
        doc_lingu_freq = {
            lingu_seq: len(doc_lingu_set)
            for lingu_seq, doc_lingu_set in lingu_occ.doc_lingu_set.items()
        }
        return DomainLinguOccurrence(
            lingu_occ.domain, lingu_occ.lingu_freq, doc_lingu_freq
        )
