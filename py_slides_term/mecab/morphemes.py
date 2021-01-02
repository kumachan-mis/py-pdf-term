from abc import ABCMeta
from dataclasses import dataclass, asdict
from typing import Dict, ClassVar


@dataclass(frozen=True)
class BaseMeCabMorpheme(metaclass=ABCMeta):
    NUM_ATTR: ClassVar[int] = 4

    surface_form: str
    pos: str
    category: str
    subcategory: str

    def __str__(self) -> str:
        return self.surface_form

    def to_json(self) -> Dict[str, str]:
        return asdict(self)

    @classmethod
    def from_json(cls, obj: Dict[str, str]):
        return cls(**obj)


@dataclass(frozen=True)
class MeCabMorphemeIPADic(BaseMeCabMorpheme):
    NUM_ATTR: ClassVar[int] = 10

    surface_form: str
    pos: str
    category: str
    subcategory: str
    subsubcategory: str
    conjugation_type: str
    conjugation_form: str
    original_form: str
    reading: str
    pronunciation: str
