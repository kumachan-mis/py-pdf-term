from dataclasses import asdict, dataclass, field
from typing import Any, Self

from .base import BaseRankingData


@dataclass(frozen=True)
class MDPRankingData(BaseRankingData):
    """Data of technical terms of a domain for MDP algorithm.

    Args
    ----
        domain:
            Domain name. (e.g., "natural language processing")
        term_freq:
            Brute force counting of lemmatized term occurrences in the domain.
            Count even if the lemmatized term occurs as a part of a lemmatized phrase.
        num_terms:
            Brute force counting of all lemmatized terms occurrences in the domain.
            Count even if the lemmatized term occurs as a part of a lemmatized phrase.
    """

    domain: str
    term_freq: dict[str, int]
    num_terms: int = field(init=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "num_terms", sum(self.term_freq.values()))

    def to_dict(self) -> dict[str, Any]:
        obj = asdict(self)
        obj.pop("num_terms", None)
        return obj

    @classmethod
    def from_dict(cls, obj: dict[str, Any]) -> Self:
        obj.pop("num_terms", None)
        return cls(**obj)
