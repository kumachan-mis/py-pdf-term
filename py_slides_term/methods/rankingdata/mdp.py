from dataclasses import dataclass, field
from typing import Dict

from .base import BaseRankingData


@dataclass(frozen=True)
class MDPRankingData(BaseRankingData):
    domain: str
    # unique domain name
    term_freq: Dict[str, int]
    # brute force counting of term occurrences in the domain
    # count even if the term occurs as a part of a phrase
    num_terms: int = field(init=False)
    # brute force counting of all terms occurrences in the domain
    # count even if the term occurs as a part of a phrase

    def __post_init__(self):
        object.__setattr__(self, "num_terms", sum(self.term_freq.values()))
