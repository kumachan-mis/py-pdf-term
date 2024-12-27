from dataclasses import dataclass
from typing import Any, Self

from .base import BaseRankingData


@dataclass(frozen=True)
class MCValueRankingData(BaseRankingData):
    """Data of technical terms of a domain for MC-Value algorithm.

    Args
    ----
        domain:
            Domain name. (e.g., "natural language processing")
        term_freq:
            Brute force counting of lemmatized term occurrences in the domain.
            Count even if the lemmatized term occurs as a part of a lemmatized phrase.
        container_terms:
            Set of containers of the lemmatized term in the domain.
            (term, container) is valid iff the container contains the term as a proper
            subsequence.
    """

    domain: str
    term_freq: dict[str, int]
    container_terms: dict[str, set[str]]

    def to_dict(self) -> dict[str, Any]:
        container_terms = {
            term: list(containers) for term, containers in self.container_terms.items()
        }
        return {
            "domain": self.domain,
            "term_freq": self.term_freq,
            "container_terms": container_terms,
        }

    @classmethod
    def from_dict(cls, obj: dict[str, Any]) -> Self:
        container_terms = {
            term: set(containers) for term, containers in obj["container_terms"].items()
        }
        return cls(obj["domain"], obj["term_freq"], container_terms)
