from dataclasses import dataclass
from typing import Any, Self

from py_pdf_term._common.data import ScoredTerm


@dataclass(frozen=True)
class MethodTermRanking:
    """Domain name and ranking of technical terms of the domain.

    Args
    ----
        domain:
            Domain name. (e.g., "natural language processing")
        ranking:
            List of pairs of lemmatized term and method score.
            The list is sorted by the score in descending order.
    """

    domain: str
    ranking: list[ScoredTerm]

    def to_dict(self) -> dict[str, Any]:
        return {
            "domain": self.domain,
            "ranking": list(map(lambda term: term.to_dict(), self.ranking)),
        }

    @classmethod
    def from_dict(cls, obj: dict[str, Any]) -> Self:
        return cls(
            obj["domain"],
            list(map(lambda item: ScoredTerm.from_dict(item), obj["ranking"])),
        )
