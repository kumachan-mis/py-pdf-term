from dataclasses import dataclass
from typing import List, Dict, Any, Type

from pdf_slides_term.mecab.morphemes import BaseMeCabMorpheme, MeCabMorphemeIPADic


@dataclass(frozen=True)
class ScoredTerm:
    term: str
    score: float

    def __str__(self) -> str:
        return self.term

    def to_json(self) -> Dict[str, Any]:
        return {"term": self.term, "score": self.score}

    @classmethod
    def from_json(
        cls,
        obj: Dict[str, Any],
        morpheme_cls: Type[BaseMeCabMorpheme] = MeCabMorphemeIPADic,
    ):
        return cls(obj["term"], obj["score"])


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
    def from_json(
        cls,
        obj: Dict[str, Any],
        morpheme_cls: Type[BaseMeCabMorpheme] = MeCabMorphemeIPADic,
    ):
        return cls(
            obj["domain"],
            list(
                map(
                    lambda item: ScoredTerm.from_json(item, morpheme_cls),
                    obj["ranking"],
                )
            ),
        )
