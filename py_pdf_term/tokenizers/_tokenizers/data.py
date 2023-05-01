from dataclasses import asdict, dataclass
from typing import Any, ClassVar, Dict


@dataclass
class Token:
    """A token in a text.

    Args
    ----
        lang:
            Language of the token. (e.g., "en", "ja")
        surface_form:
            Surface form of the token.
        pos:
            Part-of-speech tag of the token.
        category:
            Category of the token.
        subcategory:
            Subcategory of the token.
        lemma:
            Lemmatized form of the token.
        is_meaningless:
            Whether the token is meaningless or not. This is calculated by
            MeaninglessMarker.
    """

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
