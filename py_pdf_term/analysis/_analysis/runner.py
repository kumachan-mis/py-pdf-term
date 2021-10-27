from typing import Callable, TypeVar

from py_pdf_term._common.data import Term
from py_pdf_term.candidates import DomainCandidateTermList

AnalysisResult = TypeVar("AnalysisResult")


class AnalysisRunner:
    def __init__(self, ignore_augmented: bool = True) -> None:
        self._ignore_augmented = ignore_augmented

    def run_through_candidates(
        self,
        domain_candidates: DomainCandidateTermList,
        initial_result: AnalysisResult,
        update_result: Callable[[AnalysisResult, int, int, Term], None],
    ) -> AnalysisResult:
        result = initial_result

        for pdf_id, pdf_candidates in enumerate(domain_candidates.pdfs):
            for page_candidates in pdf_candidates.pages:
                page_num = page_candidates.page_num
                for candidate in page_candidates.candidates:
                    if self._ignore_augmented and candidate.augmented:
                        continue
                    update_result(result, pdf_id, page_num, candidate)

        return result

    def run_through_subcandidates(
        self,
        domain_candidates: DomainCandidateTermList,
        initial_result: AnalysisResult,
        update_result: Callable[[AnalysisResult, int, int, Term], None],
    ) -> AnalysisResult:
        result = initial_result

        for pdf_id, pdf_candidates in enumerate(domain_candidates.pdfs):
            for page_candidates in pdf_candidates.pages:
                page_num = page_candidates.page_num
                for candidate in page_candidates.candidates:
                    if self._ignore_augmented and candidate.augmented:
                        continue

                    num_tokens = len(candidate.tokens)
                    for i in range(num_tokens):
                        for j in range(i + 1, num_tokens + 1):
                            subcandidate = Term(
                                candidate.tokens[i:j],
                                candidate.fontsize,
                                candidate.ncolor,
                                candidate.augmented,
                            )
                            update_result(result, pdf_id, page_num, subcandidate)

        return result
