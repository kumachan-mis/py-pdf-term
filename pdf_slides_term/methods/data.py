from dataclasses import dataclass
from typing import List, Dict, Callable

from pdf_slides_term.share.data import TechnicalTerm
from pdf_slides_term.mecab.morphemes import BaseMeCabMorpheme, MeCabMorphemeIPADic


@dataclass
class ScoredTerm:
    term: TechnicalTerm
    score: float

    def to_json(self) -> Dict:
        return {"term": self.term.to_json(), "score": self.score}

    @classmethod
    def from_json(
        cls,
        obj: Dict,
        morpheme_cls: Callable[[str], BaseMeCabMorpheme] = MeCabMorphemeIPADic,
    ):
        return cls(TechnicalTerm.from_json(obj["term"], morpheme_cls), obj["score"])


@dataclass
class DomainTermRanking:
    domain: str
    ranking: List[ScoredTerm]

    def to_json(self) -> Dict:
        return {
            "domain": self.domain,
            "ranking": list(map(lambda term: term.to_json(), self.ranking)),
        }

    @classmethod
    def from_json(
        cls,
        obj: Dict,
        morpheme_cls: Callable[[str], BaseMeCabMorpheme] = MeCabMorphemeIPADic,
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
