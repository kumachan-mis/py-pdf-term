from dataclasses import dataclass
from typing import Tuple, Set, Dict

from pdf_slides_term.analysis.runner import AnalysisRunner
from pdf_slides_term.candidates.data import DomainCandidateTermList
from pdf_slides_term.share.data import TechnicalTerm, LinguSeq


@dataclass(frozen=True)
class TermOccurrence:
    term_freq: Dict[str, int]
    # brute force counting of term occurrences in the domain
    # count even if the term occurs as a part of a phrase
    lingu_freq: Dict[LinguSeq, int]
    # brute force counting of linguistic sequence occurrences in the domain
    # count even if the term occurs as a part of a phrase
    doc_term_freq: Dict[str, int]
    # number of documents in the domain that contain the term
    # count even if the term occurs as a part of a phrase
    doc_lingu_freq: Dict[LinguSeq, int]
    # number of documents in the domain that contain the linguistic sequence
    # count even if the term occurs as a part of a phrase


class TermOccurrenceAnalyzer:

    # public
    def __init__(self, ignore_augmented: bool = True):
        self._runner = AnalysisRunner(ignore_augmented=ignore_augmented)

    def analyze(self, domain_candidates: DomainCandidateTermList) -> TermOccurrence:
        domain_candidates_set = domain_candidates.to_domain_candidate_term_set()

        def update(
            result: Tuple[
                Dict[str, int],
                Dict[LinguSeq, int],
                Dict[str, Set[int]],
                Dict[LinguSeq, Set[int]],
            ],
            xml_id: int,
            page_num: int,
            sub_candidate: TechnicalTerm,
        ):
            sub_candidate_str = str(sub_candidate)
            if sub_candidate_str not in domain_candidates_set:
                return

            result[0][sub_candidate_str] = result[0].get(sub_candidate_str, 0) + 1

            sub_lingu_seq = sub_candidate.linguistic_sequence()
            result[1][sub_lingu_seq] = result[1].get(sub_lingu_seq, 0) + 1

            sub_candidate_doc_term_set = result[2].get(sub_candidate_str, set())
            sub_candidate_doc_term_set.add(xml_id)
            result[2][sub_candidate_str] = sub_candidate_doc_term_set

            sub_candidate_doc_lingu_set = result[3].get(sub_lingu_seq, set())
            sub_candidate_doc_lingu_set.add(xml_id)
            result[3][sub_lingu_seq] = sub_candidate_doc_lingu_set

        (
            term_freq,
            lingu_freq,
            doc_term_set,
            doc_lingu_set,
        ) = self._runner.run_through_subcandidates(
            domain_candidates, (dict(), dict(), dict(), dict()), update
        )
        doc_term_freq = {
            candidate_str: len(candidate_doc_term_set)
            for candidate_str, candidate_doc_term_set in doc_term_set.items()
        }
        doc_lingu_freq = {
            lingu_seq: len(candidate_doc_lingu_set)
            for lingu_seq, candidate_doc_lingu_set in doc_lingu_set.items()
        }
        return TermOccurrence(term_freq, lingu_freq, doc_term_freq, doc_lingu_freq)

    def analyze_term_freq(
        self, domain_candidates: DomainCandidateTermList
    ) -> Dict[str, int]:
        domain_candidates_set = domain_candidates.to_domain_candidate_term_set()

        def update(
            term_freq: Dict[str, int],
            xml_id: int,
            page_num: int,
            sub_candidate: TechnicalTerm,
        ):
            sub_candidate_str = str(sub_candidate)
            if sub_candidate_str not in domain_candidates_set:
                return
            term_freq[sub_candidate_str] = term_freq.get(sub_candidate_str, 0) + 1

        term_freq = self._runner.run_through_subcandidates(
            domain_candidates, dict(), update
        )
        return term_freq

    def analyze_lingu_freq(
        self, domain_candidates: DomainCandidateTermList
    ) -> Dict[LinguSeq, int]:
        domain_candidates_set = domain_candidates.to_domain_candidate_term_set()

        def update(
            lingu_freq: Dict[LinguSeq, int],
            xml_id: int,
            page_num: int,
            sub_candidate: TechnicalTerm,
        ):
            if str(sub_candidate) not in domain_candidates_set:
                return
            sub_lingu_seq = sub_candidate.linguistic_sequence()
            lingu_freq[sub_lingu_seq] = lingu_freq.get(sub_lingu_seq, 0) + 1

        lingu_freq = self._runner.run_through_subcandidates(
            domain_candidates, dict(), update
        )
        return lingu_freq

    def analyze_doc_term_freq(
        self, domain_candidates: DomainCandidateTermList
    ) -> Dict[str, int]:
        domain_candidates_set = domain_candidates.to_domain_candidate_term_set()

        def update(
            doc_term_set: Dict[str, Set[int]],
            xml_id: int,
            page_num: int,
            sub_candidate: TechnicalTerm,
        ):
            sub_candidate_str = str(sub_candidate)
            if sub_candidate_str not in domain_candidates_set:
                return
            sub_candidate_doc_term_set = doc_term_set.get(sub_candidate_str, set())
            sub_candidate_doc_term_set.add(xml_id)
            doc_term_set[sub_candidate_str] = sub_candidate_doc_term_set

        doc_term_set = self._runner.run_through_subcandidates(
            domain_candidates, dict(), update
        )
        doc_term_freq = {
            candidate_str: len(candidate_doc_term_set)
            for candidate_str, candidate_doc_term_set in doc_term_set.items()
        }
        return doc_term_freq

    def analyze_doc_lingu_freq(
        self, domain_candidates: DomainCandidateTermList
    ) -> Dict[LinguSeq, int]:
        domain_candidates_set = domain_candidates.to_domain_candidate_term_set()

        def update(
            doc_lingu_set: Dict[LinguSeq, Set[int]],
            xml_id: int,
            page_num: int,
            sub_candidate: TechnicalTerm,
        ):
            if str(sub_candidate) not in domain_candidates_set:
                return
            sub_lingu_seq = sub_candidate.linguistic_sequence()
            sub_candidate_doc_lingu_set = doc_lingu_set.get(sub_lingu_seq, set())
            sub_candidate_doc_lingu_set.add(xml_id)
            doc_lingu_set[sub_lingu_seq] = sub_candidate_doc_lingu_set

        doc_lingu_set = self._runner.run_through_subcandidates(
            domain_candidates, dict(), update
        )
        doc_lingu_freq = {
            lingu_seq: len(candidate_doc_lingu_set)
            for lingu_seq, candidate_doc_lingu_set in doc_lingu_set.items()
        }
        return doc_lingu_freq
