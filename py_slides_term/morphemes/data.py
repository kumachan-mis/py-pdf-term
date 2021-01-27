from abc import ABCMeta
from dataclasses import dataclass, asdict
from typing import Dict, ClassVar


@dataclass(frozen=True)
class BaseMorpheme(metaclass=ABCMeta):
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
class MorphemeSpaCyDic(BaseMorpheme):
    NUM_ATTR: ClassVar[int] = 6

    surface_form: str
    pos: str
    category: str
    subcategory: str
    subsubcategory: str
    universal_tag: str
    dep_relations: str
    original_form: str
    shape: str
    is_stop: bool
