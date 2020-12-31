from dataclasses import dataclass
from typing import TypeVar


@dataclass(frozen=True)
class BaseRankingData:
    domain: str
    # unique domain name


RankingData = TypeVar("RankingData", bound=BaseRankingData)
