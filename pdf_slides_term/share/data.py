import re
from dataclasses import dataclass
from typing import List, Dict, Any, Type

from pdf_slides_term.mecab.morphemes import BaseMeCabMorpheme, MeCabMorphemeIPADic
from pdf_slides_term.share.consts import HIRAGANA_REGEX, KATAKANA_REGEX, KANJI_REGEX


JAPANESE_REGEX = rf"({HIRAGANA_REGEX}|{KATAKANA_REGEX}|{KANJI_REGEX})"


@dataclass(frozen=True)
class TechnicalTerm:
    morphemes: List[BaseMeCabMorpheme]
    fontsize: float = 0
    augmented: bool = False

    def __str__(self) -> str:
        num_morphemes = len(self.morphemes)
        if not num_morphemes:
            return ""

        japanese_regex = re.compile(rf"{JAPANESE_REGEX}*")
        term_str = self.morphemes[0].surface_form
        for i in range(1, num_morphemes):
            if (
                japanese_regex.fullmatch(self.morphemes[i - 1].surface_form) is None
                or japanese_regex.fullmatch(self.morphemes[i].surface_form) is None
            ):
                term_str += " "

            term_str += self.morphemes[i].surface_form

        return term_str

    def to_json(self) -> Dict[str, Any]:
        return {
            "morphemes": list(map(lambda morpheme: morpheme.to_json(), self.morphemes)),
            "fontsize": self.fontsize,
            "augmented": self.augmented,
        }

    @classmethod
    def from_json(
        cls,
        obj: Dict[str, Any],
        morpheme_cls: Type[BaseMeCabMorpheme] = MeCabMorphemeIPADic,
    ):
        return cls(
            list(map(lambda item: morpheme_cls.from_json(item), obj["morphemes"])),
            obj.get("fontsize", 0),
            obj.get("augmented", False),
        )
