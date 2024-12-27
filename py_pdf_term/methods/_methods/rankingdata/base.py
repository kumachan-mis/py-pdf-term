from dataclasses import asdict, dataclass
from typing import Any, Self


@dataclass(frozen=True)
class BaseRankingData:
    """Base class for ranking data of technical terms of a domain.

    Args
    ----
        domain:
            Domain name. (e.g., "natural language processing")
    """

    domain: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, obj: dict[str, Any]) -> Self:
        return cls(**obj)
