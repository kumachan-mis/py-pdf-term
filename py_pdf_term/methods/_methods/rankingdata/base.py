from dataclasses import dataclass, asdict
from typing import Dict, Any, TypeVar


@dataclass(frozen=True)
class BaseRankingData:
    domain: str
    # unique domain name

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> "BaseRankingData":
        return cls(**obj)


RankingData = TypeVar("RankingData", bound=BaseRankingData)