from dataclasses import dataclass

from .base import BaseRankingData


@dataclass(frozen=True)
class FLRRankingData(BaseRankingData):
    """Data of technical terms of a domain for FLR algorithm.

    Args
    ----
        domain:
            Domain name. (e.g., "natural language processing")
        term_freq:
            Brute force counting of lemmatized term occurrences in the domain.
            Count even if the lemmatized term occurs as a part of a lemmatized phrase.
        left_freq:
            Number of occurrences of lemmatized (left, token) in the domain.
            If token or left is meaningless this is fixed at zero.
        right_freq:
            Number of occurrences of lemmatized (token, right) in the domain.
            If token or right is meaningless this is fixed at zero.
    """

    domain: str
    term_freq: dict[str, int]
    left_freq: dict[str, dict[str, int]]
    right_freq: dict[str, dict[str, int]]
