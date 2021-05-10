from abc import ABCMeta
from dataclasses import dataclass, asdict
from typing import Dict, Literal, ClassVar


@dataclass(frozen=True)
class BaseMorpheme(metaclass=ABCMeta):
    NUM_ATTR: ClassVar[int] = 5

    lang: Literal["ja", "en"]
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
class SpaCyMorpheme(BaseMorpheme):
    NUM_ATTR: ClassVar[int] = 9

    lang: Literal["ja", "en"]
    surface_form: str
    pos: str
    category: str
    subcategory: str
    subsubcategory: str
    universal_tag: str
    shape: str
    is_stop: bool
