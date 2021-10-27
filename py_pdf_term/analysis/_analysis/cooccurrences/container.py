from dataclasses import dataclass
from typing import Dict, Set

from py_pdf_term._common.data import Term
from py_pdf_term.candidates import DomainCandidateTermList

from ..runner import AnalysisRunner


@dataclass(frozen=True)
class DomainContainerTerms:
    domain: str
    # unique domain name
    container_terms: Dict[str, Set[str]]
    # set of lemmatized containers of the lemmatized term in the domain
    # (term, container) is valid iff the container contains the term
    # as a proper subsequence


class ContainerTermsAnalyzer:
    def __init__(self, ignore_augmented: bool = True) -> None:
        self._runner = AnalysisRunner(ignore_augmented=ignore_augmented)

    def analyze(
        self, domain_candidates: DomainCandidateTermList
    ) -> DomainContainerTerms:
        domain_candidates_set = domain_candidates.to_candidates_str_set(
            lambda candidate: candidate.lemma()
        )

        def update(
            container_terms: DomainContainerTerms,
            pdf_id: int,
            page_num: int,
            candidate: Term,
        ) -> None:
            candidate_lemma = candidate.lemma()
            container_terms.container_terms[
                candidate_lemma
            ] = container_terms.container_terms.get(candidate_lemma, set())

            num_tokens = len(candidate.tokens)
            for i in range(num_tokens):
                jstart, jstop = i + 1, (num_tokens + 1 if i > 0 else num_tokens)
                for j in range(jstart, jstop):
                    subcandidate = Term(
                        candidate.tokens[i:j],
                        candidate.fontsize,
                        candidate.ncolor,
                        candidate.augmented,
                    )
                    subcandidate_lemma = subcandidate.lemma()
                    if subcandidate_lemma not in domain_candidates_set:
                        continue

                    container_term_set = container_terms.container_terms.get(
                        subcandidate_lemma, set()
                    )
                    container_term_set.add(candidate_lemma)
                    container_terms.container_terms[
                        subcandidate_lemma
                    ] = container_term_set

        container_terms = self._runner.run_through_candidates(
            domain_candidates,
            DomainContainerTerms(domain_candidates.domain, dict()),
            update,
        )
        return container_terms
