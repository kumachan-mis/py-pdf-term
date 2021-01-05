from dataclasses import dataclass, asdict
from typing import Dict, Any, TypeVar, Type


@dataclass(frozen=True)
class BaseRankingData:
    domain: str
    # unique domain name

    def to_json(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_json(cls: Type["RankingData"], obj: Dict[str, Any]) -> "RankingData":
        return cls(**obj)


RankingData = TypeVar("RankingData", bound=BaseRankingData)
