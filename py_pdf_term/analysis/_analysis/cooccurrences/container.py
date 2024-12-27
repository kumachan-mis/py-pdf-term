from dataclasses import dataclass

from py_pdf_term.candidates import DomainCandidateTermList
from py_pdf_term.tokenizers import Term

from ..runner import AnalysisRunner


@dataclass(frozen=True)
class DomainContainerTerms:
    """Domain name and container terms of the domain.

    Args
    ----
        domain:
            Domain name. (e.g., "natural language processing")
        container_terms:
            Set of lemmatized containers of the lemmatized term in the domain.
            (term, container) is valid if and only if the container contains the term as
            a proper subsequence.
    """

    domain: str
    container_terms: dict[str, set[str]]


class ContainerTermsAnalyzer:
    """Analyze container terms of the domain.

    Args
    ----
        ignore_augmented:
            If True, ignore augmented terms. The default is True.
    """

    def __init__(self, ignore_augmented: bool = True) -> None:
        self._runner = AnalysisRunner[DomainContainerTerms](
            ignore_augmented=ignore_augmented
        )

    def analyze(
        self, domain_candidates: DomainCandidateTermList
    ) -> DomainContainerTerms:
        """Analyze container terms of the domain.

        Args
        ----
            domain_candidates:
                List of candidate terms in a domain. The target of analysis.

        Returns
        -------
            DomainContainerTerms:
                Domain name and container terms of candidate terms in the domain.
        """

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
            container_terms.container_terms[candidate_lemma] = (
                container_terms.container_terms.get(candidate_lemma, set())
            )

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
                    container_terms.container_terms[subcandidate_lemma] = (
                        container_term_set
                    )

        container_terms = self._runner.run_through_candidates(
            domain_candidates,
            DomainContainerTerms(domain_candidates.domain, dict()),
            update,
        )
        return container_terms
