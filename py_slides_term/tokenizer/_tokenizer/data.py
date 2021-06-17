from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional


@dataclass(frozen=True)
class Morpheme:
    lang: str
    surface_form: str
    pos: str
    category: Optional[str]
    subcategory: Optional[str]
    lemma: str

    def __str__(self) -> str:
        return self.surface_form

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> "Morpheme":
        return cls(**obj)
