from dataclasses import asdict, dataclass
from typing import Any, ClassVar, Dict


@dataclass(frozen=True)
class Token:
    NUM_ATTR: ClassVar[int] = 10

    lang: str
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
    def from_dict(cls, obj: Dict[str, Any]) -> "Token":
        return cls(**obj)
