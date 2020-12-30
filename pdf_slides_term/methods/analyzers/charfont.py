from dataclasses import dataclass
from typing import Dict, Callable, TypeVar

from pdf_slides_term.candidates.data import DomainCandidateTermList
from pdf_slides_term.share.data import TechnicalTerm


@dataclass(frozen=True)
class TermCharFont:
    term_maxsize: Dict[str, float]
    # max fontsize of the term in the domain
    # default of this is zero


class TermCharFontAnalyzer:
    _AnalysisResult = TypeVar("_AnalysisResult")

    # public
    def __init__(self, ignore_augmented: bool = True):
        self._ignore_augmented = ignore_augmented

    def analyze(self, domain_candidates: DomainCandidateTermList) -> TermCharFont:
        return TermCharFont(self.analyze_term_maxsize(domain_candidates))

    def analyze_term_maxsize(
        self, domain_candidates: DomainCandidateTermList
    ) -> Dict[str, float]:
        def update(
            term_maxsize: Dict[str, float],
            xml_id: int,
            page_num: int,
            sub_candidate: TechnicalTerm,
        ):
            sub_candidate_str = str(sub_candidate)
            term_maxsize[sub_candidate_str] = max(
                term_maxsize.get(sub_candidate_str, 0),
                sub_candidate.fontsize,
            )

        term_maxsize = self._run_brute_force_analysis(domain_candidates, dict(), update)
        return term_maxsize

    # private
    def _run_brute_force_analysis(
        self,
        domain_candidates: DomainCandidateTermList,
        initial_result: _AnalysisResult,
        update_result: Callable[
            [_AnalysisResult, int, int, TechnicalTerm],
            None,
        ],
    ) -> _AnalysisResult:
        domain_candidates_dict = domain_candidates.to_domain_candidate_term_dict()
        result = initial_result

        for xml_id, xml_candidates in enumerate(domain_candidates.xmls):
            for page_candidates in xml_candidates.pages:
                page_num = page_candidates.page_num
                for candidate in page_candidates.candidates:
                    if self._ignore_augmented and candidate.augmented:
                        continue

                    num_morphemes = len(candidate.morphemes)
                    for i in range(num_morphemes):
                        for j in range(i + 1, num_morphemes + 1):
                            sub_candidate = TechnicalTerm(
                                candidate.morphemes[i:j],
                                candidate.fontsize,
                                candidate.augmented,
                            )
                            if str(sub_candidate) in domain_candidates_dict:
                                update_result(result, xml_id, page_num, sub_candidate)

        return result
