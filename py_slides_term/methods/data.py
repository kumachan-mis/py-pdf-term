from dataclasses import dataclass
from typing import List, Dict, Any

from py_slides_term.share.data import ScoredTerm


@dataclass(frozen=True)
class MethodTermRanking:
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
