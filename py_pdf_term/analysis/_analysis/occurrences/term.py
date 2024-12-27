from dataclasses import dataclass

from py_pdf_term.candidates import DomainCandidateTermList
from py_pdf_term.tokenizers import Term

from ..runner import AnalysisRunner


@dataclass(frozen=True)
class DomainTermOccurrence:
    """Domain name and term occurrence of the domain

    Args
    ----
        domain:
            Domain name. (e.g., "natural language processing")
        term_freq:
            Brute force counting of lemmatized term occurrences in the domain.
            Count even if the lemmatized term occurs as a part of a lemmatized phrase.
        doc_term_freq:
            Number of documents in the domain that contain the lemmatized term.
            Count even if the lemmatized term occurs as a part of a lemmatized phrase.
    """

    domain: str
    term_freq: dict[str, int]
    doc_term_freq: dict[str, int]


@dataclass(frozen=True)
class _DomainTermOccurrence:
    """Domain name and term occurrence of the domain

    Args
    ----
        domain:
            Domain name. (e.g., "natural language processing")
        term_freq:
            Brute force counting of lemmatized term occurrences in the domain.
            Count even if the lemmatized term occurs as a part of a lemmatized phrase.
        doc_term_set:
            Set of document IDs in the domain that contain the lemmatized term.
            Add even if the lemmatized term occurs as a part of a lemmatized phrase.
    """

    domain: str
    term_freq: dict[str, int]
    doc_term_set: dict[str, set[int]]


class TermOccurrenceAnalyzer:
    """Analyze term occurrences in a domain.

    Args
    ----
        ignore_augmented:
            If True, ignore augmented terms. The default is True.
    """

    def __init__(self, ignore_augmented: bool = True) -> None:
        self._runner = AnalysisRunner[_DomainTermOccurrence](
            ignore_augmented=ignore_augmented
        )

    def analyze(
        self, domain_candidates: DomainCandidateTermList
    ) -> DomainTermOccurrence:
        """Analyze term occurrences in a domain.

        Args
        ----
            domain_candidates:
                List of candidate terms in a domain. The target of analysis.

        Returns
        -------
            DomainTermOccurrence:
                Domain name and term occurrence of candidate terms in the domain.
        """

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
