from dataclasses import dataclass, asdict
from typing import List, Dict, Any


@dataclass(frozen=True)
class ScoredTerm:
    term: str
    score: float

    def __str__(self) -> str:
        return self.term

    def to_json(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_json(cls, obj: Dict[str, Any]):
        return cls(**obj)


@dataclass(frozen=True)
class DomainTermRanking:
    domain: str
    ranking: List[ScoredTerm]

    def to_json(self) -> Dict[str, Any]:
        return {
            "domain": self.domain,
            "ranking": list(map(lambda term: term.to_json(), self.ranking)),
        }

    @classmethod
    def from_json(cls, obj: Dict[str, Any]):
        return cls(
            obj["domain"],
            list(map(lambda item: ScoredTerm.from_json(item), obj["ranking"])),
        )
