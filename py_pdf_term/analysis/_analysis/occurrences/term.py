from dataclasses import dataclass
from typing import Dict, Set

from py_pdf_term._common.data import Term
from py_pdf_term.candidates import DomainCandidateTermList

from ..runner import AnalysisRunner


@dataclass(frozen=True)
class DomainTermOccurrence:
    domain: str
    # unique domain name
    term_freq: Dict[str, int]
    # brute force counting of lemmatized term occurrences in the domain
    # count even if the lemmatized term occurs as a part of a lemmatized phrase
    doc_term_freq: Dict[str, int]
    # number of documents in the domain that contain the lemmatized term
    # count even if the lemmatized term occurs as a part of a lemmatized phrase


@dataclass(frozen=True)
class _DomainTermOccurrence:
    domain: str
    # unique domain name
    term_freq: Dict[str, int]
    # brute force counting of lemmatized term occurrences in the domain
    # count even if the term occurs as a part of a lemmatized phrase
    doc_term_set: Dict[str, Set[int]]
    # set of document IDs in the domain that contain the lemmatized term
    # add even if the lemmatized term occurs as a part of a lemmatized phrase


class TermOccurrenceAnalyzer:
    def __init__(self, ignore_augmented: bool = True) -> None:
        self._runner = AnalysisRunner(ignore_augmented=ignore_augmented)

    def analyze(
        self, domain_candidates: DomainCandidateTermList
    ) -> DomainTermOccurrence:
        domain_candidates_set = domain_candidates.to_candidates_str_set(
            lambda candidate: candidate.lemma()
        )

        def update(
            term_occ: _DomainTermOccurrence,
            pdf_id: int,
            page_num: int,
            subcandidate: Term,
        ) -> None:
            subcandidate_lemma = subcandidate.lemma()
            if subcandidate_lemma not in domain_candidates_set:
                return
            term_occ.term_freq[subcandidate_lemma] = (
                term_occ.term_freq.get(subcandidate_lemma, 0) + 1
            )
            doc_term_set = term_occ.doc_term_set.get(subcandidate_lemma, set())
            doc_term_set.add(pdf_id)
            term_occ.doc_term_set[subcandidate_lemma] = doc_term_set

        term_occ = self._runner.run_through_subcandidates(
            domain_candidates,
            _DomainTermOccurrence(domain_candidates.domain, dict(), dict()),
            update,
        )
        term_occ = self._finalize(term_occ)
        return term_occ

    def _finalize(self, term_occ: _DomainTermOccurrence) -> DomainTermOccurrence:
        doc_term_freq = {
            candidate_str: len(doc_term_set)
            for candidate_str, doc_term_set in term_occ.doc_term_set.items()
        }
        return DomainTermOccurrence(term_occ.domain, term_occ.term_freq, doc_term_freq)
