from dataclasses import dataclass

from py_pdf_term.candidates import DomainCandidateTermList
from py_pdf_term.tokenizers import Term

from ..runner import AnalysisRunner


@dataclass(frozen=True)
class DomainLeftRightFrequency:
    """Domain name and left/right frequency of the domain.

    Args
    ----
        domain:
            Domain name. (e.g., "natural language processing")
        left_freq:
            Number of occurrences of lemmatized (left, token) in the domain.
            If token or left is meaningless, this is fixed at zero.
        right_freq:
            Number of occurrences of lemmatized (token, right) in the domain.
            If token or right is meaningless, this is fixed at zero.
    """

    domain: str
    left_freq: dict[str, dict[str, int]]
    right_freq: dict[str, dict[str, int]]


class TermLeftRightFrequencyAnalyzer:
    """Analyze left/right frequency of terms in a domain.

    Args
    ----
        ignore_augmented:
            If True, ignore augmented terms. The default is True.
    """

    def __init__(self, ignore_augmented: bool = True) -> None:
        self._ignore_augmented = ignore_augmented
        self._runner = AnalysisRunner[DomainLeftRightFrequency](
            ignore_augmented=ignore_augmented
        )

    def analyze(
        self, domain_candidates: DomainCandidateTermList
    ) -> DomainLeftRightFrequency:
        """Analyze left/right frequency of terms in a domain.

        Args
        ----
            domain_candidates:
                List of candidate terms in a domain. The target of analysis.

        Returns
        -------
            DomainLeftRightFrequency:
                Domain name and left/right frequency of candidate terms in the domain.
        """

        def update(
            lrfreq: DomainLeftRightFrequency,
            pdf_id: int,
            page_num: int,
            candidate: Term,
        ) -> None:
            num_tokens = len(candidate.tokens)
            for i in range(num_tokens):
                token = candidate.tokens[i]
                if token.is_meaningless:
                    lrfreq.left_freq[token.lemma] = dict()
                    lrfreq.right_freq[token.lemma] = dict()
                    continue

                self._update_left_freq(lrfreq, candidate, i)
                self._update_right_freq(lrfreq, candidate, i)

        lrfreq = self._runner.run_through_candidates(
            domain_candidates,
            DomainLeftRightFrequency(domain_candidates.domain, dict(), dict()),
            update,
        )

        return lrfreq

    def _update_left_freq(
        self, lrfreq: DomainLeftRightFrequency, candidate: Term, idx: int
    ) -> None:
        token = candidate.tokens[idx]

        if idx == 0:
            left = lrfreq.left_freq.get(token.lemma, dict())
            lrfreq.left_freq[token.lemma] = left
            return

        left_token = candidate.tokens[idx - 1]
        if not left_token.is_meaningless:
            left = lrfreq.left_freq.get(token.lemma, dict())
            left[left_token.lemma] = left.get(left_token.lemma, 0) + 1
            lrfreq.left_freq[token.lemma] = left
        else:
            left = lrfreq.left_freq.get(token.lemma, dict())
            lrfreq.left_freq[token.lemma] = left

    def _update_right_freq(
        self, lrfreq: DomainLeftRightFrequency, candidate: Term, idx: int
    ) -> None:
        num_tokens = len(candidate.tokens)
        token = candidate.tokens[idx]

        if idx == num_tokens - 1:
            right = lrfreq.right_freq.get(token.lemma, dict())
            lrfreq.right_freq[token.lemma] = right
            return

        right_token = candidate.tokens[idx + 1]
        if not right_token.is_meaningless:
            right = lrfreq.right_freq.get(token.lemma, dict())
            right[right_token.lemma] = right.get(right_token.lemma, 0) + 1
            lrfreq.right_freq[token.lemma] = right
        else:
            right = lrfreq.right_freq.get(token.lemma, dict())
            lrfreq.right_freq[token.lemma] = right
