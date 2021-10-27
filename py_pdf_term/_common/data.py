import re
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Tuple, Union

from py_pdf_term._common.consts import NOSPACE_REGEX
from py_pdf_term.tokenizer import Token

GARBAGE_SPACE = re.compile(rf"(?<={NOSPACE_REGEX}) (?=\S)|(?<=\S) (?={NOSPACE_REGEX})")


LinguSeq = Tuple[Tuple[str, str, str], ...]


@dataclass(frozen=True)
class Term:
    tokens: List[Token]
    fontsize: float = 0.0
    ncolor: str = ""
    augmented: bool = False

    @property
    def lang(self) -> Union[str, None]:
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

    def linguistic_sequence(self) -> LinguSeq:
        return tuple(
            (token.pos, token.category, token.subcategory) for token in self.tokens
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tokens": list(map(lambda token: token.to_dict(), self.tokens)),
            "fontsize": self.fontsize,
            "ncolor": self.ncolor,
            "augmented": self.augmented,
        }

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> "Term":
        return cls(
            list(map(lambda item: Token.from_dict(item), obj["tokens"])),
            obj.get("fontsize", 0),
            obj.get("ncolor", ""),
            obj.get("augmented", False),
        )


@dataclass(frozen=True)
class ScoredTerm:
    term: str
    score: float

    def __str__(self) -> str:
        return self.term

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> "ScoredTerm":
        return cls(**obj)
