from dataclasses import asdict, dataclass
from typing import Any, Dict, TypeVar


@dataclass(frozen=True)
class BaseRankingData:
    """Base class for ranking data of technical terms of a domain.

    Args
    ----
        domain:
            Domain name. (e.g., "natural language processing")
    """

    domain: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> "BaseRankingData":
        return cls(**obj)


RankingData = TypeVar("RankingData", bound=BaseRankingData)
