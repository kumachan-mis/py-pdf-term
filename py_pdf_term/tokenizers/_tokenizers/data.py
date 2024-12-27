import re
from dataclasses import asdict, dataclass
from typing import Any, ClassVar, Self

from py_pdf_term._common.consts import NOSPACE_REGEX

GARBAGE_SPACE = re.compile(rf"(?<={NOSPACE_REGEX}) (?=\S)|(?<=\S) (?={NOSPACE_REGEX})")


@dataclass
class Token:
    """Token in a text.

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

    def to_dict(self) -> dict[str, str]:
        return asdict(self)

    @classmethod
    def from_dict(cls, obj: dict[str, Any]) -> Self:
        return cls(**obj)


@dataclass(frozen=True)
class Term:
    tokens: list[Token]
    fontsize: float = 0.0
    ncolor: str = ""
    augmented: bool = False

    @property
    def lang(self) -> str | None:
        if not self.tokens:
            return None

        lang = self.tokens[0].lang
        if all(map(lambda token: token.lang == lang, self.tokens)):
            return lang

        return None

    def __str__(self) -> str:
        return GARBAGE_SPACE.sub("", " ".join(map(str, self.tokens)))

    def surface_form(self) -> str:
        return GARBAGE_SPACE.sub(
            "", " ".join(map(lambda token: token.surface_form, self.tokens))
        )

    def lemma(self) -> str:
        return GARBAGE_SPACE.sub(
            "", " ".join(map(lambda token: token.lemma, self.tokens))
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "tokens": list(map(lambda token: token.to_dict(), self.tokens)),
            "fontsize": self.fontsize,
            "ncolor": self.ncolor,
            "augmented": self.augmented,
        }

    @classmethod
    def from_dict(cls, obj: dict[str, Any]) -> Self:
        return cls(
            list(map(lambda item: Token.from_dict(item), obj["tokens"])),
            obj.get("fontsize", 0),
            obj.get("ncolor", ""),
            obj.get("augmented", False),
        )
