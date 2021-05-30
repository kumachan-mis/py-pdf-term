from dataclasses import dataclass, field
from typing import Dict

from .base import BaseRankingData


@dataclass(frozen=True)
class MDPRankingData(BaseRankingData):
    domain: str
    # unique domain name
    term_freq: Dict[str, int]
    # brute force counting of lemmatized term occurrences in the domain
    # count even if the lemmatized term occurs as a part of a lemmatized phrase
    num_terms: int = field(init=False)
    # brute force counting of all lemmatized terms occurrences in the domain
    # count even if the lemmatized term occurs as a part of a lemmatized phrase

    def __post_init__(self) -> None:
        object.__setattr__(self, "num_terms", sum(self.term_freq.values()))
