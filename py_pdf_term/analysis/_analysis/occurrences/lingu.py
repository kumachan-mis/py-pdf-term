from dataclasses import dataclass
from typing import Dict, Set

from py_pdf_term._common.data import LinguSeq, Term
from py_pdf_term.candidates import DomainCandidateTermList

from ..runner import AnalysisRunner


@dataclass(frozen=True)
class DomainLinguOccurrence:
    domain: str
    # unique domain name
    lingu_freq: Dict[LinguSeq, int]
    # brute force counting of linguistic sequence occurrences in the domain
    # count even if the lemmatized term occurs as a part of a lemmatized phrase
    doc_lingu_freq: Dict[LinguSeq, int]
    # number of documents in the domain that contain the linguistic sequence
    # count even if the lemmatized term occurs as a part of a lemmatized phrase


@dataclass(frozen=True)
class _DomainLinguOccurrence:
    domain: str
    # unique domain name
    lingu_freq: Dict[LinguSeq, int]
    # brute force counting of linguistic sequence occurrences in the domain
    # count even if the lemmatized term occurs as a part of a lemmatized phrase
    doc_lingu_set: Dict[LinguSeq, Set[int]]
    # set of document IDs in the domain that contain the linguistic sequence
    # add even if the lemmatized term occurs as a part of a lemmatized phrase


class LinguOccurrenceAnalyzer:
    def __init__(self, ignore_augmented: bool = True) -> None:
        self._runner = AnalysisRunner(ignore_augmented=ignore_augmented)

    def analyze(
        self, domain_candidates: DomainCandidateTermList
    ) -> DomainLinguOccurrence:
        domain_candidates_set = domain_candidates.to_candidates_str_set(
            lambda candidate: candidate.lemma()
        )

        def update(
            lingu_occ: _DomainLinguOccurrence,
            pdf_id: int,
            page_num: int,
            subcandidate: Term,
        ) -> None:
            if subcandidate.lemma() not in domain_candidates_set:
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

    def _finalize(self, lingu_occ: _DomainLinguOccurrence) -> DomainLinguOccurrence:
        doc_lingu_freq = {
            lingu_seq: len(doc_lingu_set)
            for lingu_seq, doc_lingu_set in lingu_occ.doc_lingu_set.items()
        }
        return DomainLinguOccurrence(
            lingu_occ.domain, lingu_occ.lingu_freq, doc_lingu_freq
        )
