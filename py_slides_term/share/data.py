import re
from dataclasses import dataclass, asdict
from typing import List, Tuple, Dict, Any, Union

from py_slides_term.tokenizer import Morpheme, Language
from py_slides_term.share.consts import JAPANESE_REGEX


LinguSeq = Tuple[Tuple[str, str, str], ...]


@dataclass(frozen=True)
class Term:
    morphemes: List[Morpheme]
    fontsize: float = 0.0
    ncolor: str = ""
    augmented: bool = False

    @property
    def lang(self) -> Union[Language, None]:
        if not self.morphemes:
            return None

        lang = self.morphemes[0].lang
        if all(map(lambda morpheme: morpheme.lang == lang, self.morphemes)):
            return lang

        return None

    def __str__(self) -> str:
        num_morphemes = len(self.morphemes)
        if not num_morphemes:
            return ""

        japanese_regex = re.compile(rf"{JAPANESE_REGEX}*")
        hyphen_regex = re.compile("-")

        term_str = str(self.morphemes[0])
        for i in range(1, num_morphemes):
            prev_morpheme_str = str(self.morphemes[i - 1])
            morpheme_str = str(self.morphemes[i])
            if (
                japanese_regex.fullmatch(prev_morpheme_str) is None
                or japanese_regex.fullmatch(morpheme_str) is None
            ) and (
                hyphen_regex.fullmatch(prev_morpheme_str) is None
                and hyphen_regex.fullmatch(morpheme_str) is None
            ):
                term_str += " "

            term_str += morpheme_str

        return term_str

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
    def from_dict(cls, obj: Dict[str, Any]):
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
    def from_dict(cls, obj: Dict[str, Any]):
        return cls(**obj)
