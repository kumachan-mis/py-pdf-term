from dataclasses import asdict, dataclass
from typing import Any, ClassVar, Dict


@dataclass
class Token:
    NUM_ATTR: ClassVar[int] = 6

    lang: str
    surface_form: str
    pos: str
    category: str
    subcategory: str
    lemma: str
    is_meaningless: bool = False

    def __str__(self) -> str:
        return self.surface_form

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> "Token":
        return cls(**obj)
