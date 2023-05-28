from dataclasses import dataclass

from .base import BaseRankingData


@dataclass(frozen=True)
class TFIDFRankingData(BaseRankingData):
    """Data of technical terms of a domain for TF-IDF algorithm.

    Args
    ----
        domain:
            Domain name. (e.g., "natural language processing")
        term_freq:
            Brute force counting of lemmatized term occurrences in the domain.
            Count even if the lemmatized term occurs as a part of a lemmatized phrase.
        doc_freq:
            Number of documents in the domain that contain the lemmatized term.
            Count even if the lemmatized term occurs as a part of a lemmatized phrase.
        num_docs:
            Number of documents in the domain.
    """

    domain: str
    term_freq: dict[str, int]
    doc_freq: dict[str, int]
    num_docs: int
