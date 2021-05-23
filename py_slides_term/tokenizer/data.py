from dataclasses import dataclass, asdict
from typing import Dict, Literal, ClassVar


Language = Literal["ja", "en"]


@dataclass(frozen=True)
class Morpheme:
    NUM_ATTR: ClassVar[int] = 10

    lang: Language
    surface_form: str
    pos: str
    category: str
    subcategory: str
    subsubcategory: str
    universal_tag: str
    lemma: str
    shape: str
    is_stop: bool

    def __str__(self) -> str:
        return self.surface_form

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)

    @classmethod
    def from_dict(cls, obj: Dict[str, str]):
        return cls(**obj)
