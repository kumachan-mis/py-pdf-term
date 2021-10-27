from dataclasses import dataclass
from typing import Any, Dict, Set

from .base import BaseRankingData


@dataclass(frozen=True)
class MCValueRankingData(BaseRankingData):
    domain: str
    # unique domain name
    term_freq: Dict[str, int]
    # brute force counting of lemmatized term occurrences in the domain
    # count even if the lemmatized term occurs as a part of a lemmatized phrase
    container_terms: Dict[str, Set[str]]
    # set of containers of the lemmatized term in the domain
    # (term, container) is valid iff the container contains the term
    # as a proper subsequence

    def to_dict(self) -> Dict[str, Any]:
        container_terms = {
            term: list(containers) for term, containers in self.container_terms.items()
        }
        return {
            "domain": self.domain,
            "term_freq": self.term_freq,
            "container_terms": container_terms,
        }

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> "MCValueRankingData":
        container_terms = {
            term: set(containers) for term, containers in obj["container_terms"].items()
        }
        return MCValueRankingData(obj["domain"], obj["term_freq"], container_terms)
