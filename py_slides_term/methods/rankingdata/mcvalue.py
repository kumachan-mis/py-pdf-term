from dataclasses import dataclass
from typing import Set, Dict, Any

from .base import BaseRankingData


@dataclass(frozen=True)
class MCValueRankingData(BaseRankingData):
    domain: str
    # unique domain name
    term_freq: Dict[str, int]
    # brute force counting of term occurrences in the domain
    # count even if the term occurs as a part of a phrase
    container_terms: Dict[str, Set[str]]
    # set of containers of the term in the domain
    # (term, container) is valid iff the container contains the term
    # as a proper subsequence

    def to_json(self) -> Dict[str, Any]:
        container_terms = {
            term: list(containers) for term, containers in self.container_terms.items()
        }
        return {
            "domain": self.domain,
            "term_freq": self.term_freq,
            "container_terms": container_terms,
        }

    @classmethod
    def from_json(cls, obj: Dict[str, Any]):
        container_terms = {
            term: set(containers) for term, containers in obj["container_terms"].items()
        }
        return MCValueRankingData(obj["domain"], obj["term_freq"], container_terms)
