from dataclasses import dataclass
from typing import List, Dict

from pdf_slides_term.share.data import TechnicalTerm


@dataclass
class ScoredTerm:
    term: TechnicalTerm
    score: float

    def to_json(self) -> Dict:
        return {"term": self.term.to_json(), "score": self.score}


@dataclass
class DomainTermRanking:
    domain: str
    ranking: List[ScoredTerm]

    def to_json(self) -> Dict:
        return {
            "domain": self.domain,
            "ranking": list(map(lambda term: term.to_json(), self.ranking)),
        }
