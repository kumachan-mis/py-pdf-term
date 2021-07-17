import re
from dataclasses import dataclass, asdict
from typing import List, Tuple, Dict, Any, Union

from py_pdf_term.tokenizer import Morpheme
from py_pdf_term._common.consts import NOSPACE_REGEX

GARBAGE_SPACE = re.compile(rf"(?<={NOSPACE_REGEX}) (?=\S)|(?<=\S) (?={NOSPACE_REGEX})")


LinguSeq = Tuple[Tuple[str, str, str], ...]


@dataclass(frozen=True)
class Term:
    morphemes: List[Morpheme]
    fontsize: float = 0.0
    ncolor: str = ""
    augmented: bool = False

    @property
    def lang(self) -> Union[str, None]:
        if not self.morphemes:
            return None

        lang = self.morphemes[0].lang
        if all(map(lambda morpheme: morpheme.lang == lang, self.morphemes)):
            return lang

        return None

    def __str__(self) -> str:
        return GARBAGE_SPACE.sub("", " ".join(map(str, self.morphemes)))

    def surface_form(self) -> str:
        return GARBAGE_SPACE.sub(
            "", " ".join(map(lambda morpheme: morpheme.surface_form, self.morphemes))
        )

    def lemma(self) -> str:
        return GARBAGE_SPACE.sub(
            "", " ".join(map(lambda morpheme: morpheme.lemma, self.morphemes))
        )

    def linguistic_sequence(self) -> LinguSeq:
        return tuple(
            (morpheme.pos, morpheme.category, morpheme.subcategory)
            for morpheme in self.morphemes
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "morphemes": list(map(lambda morpheme: morpheme.to_dict(), self.morphemes)),
            "fontsize": self.fontsize,
            "ncolor": self.ncolor,
            "augmented": self.augmented,
        }

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> "Term":
        return cls(
            list(map(lambda item: Morpheme.from_dict(item), obj["morphemes"])),
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
