import re
from typing import List

from .base import BaseCandidateMorphemeFilter
from py_pdf_term.tokenizer import Morpheme
from py_pdf_term._common.consts import ENGLISH_REGEX, NUMBER_REGEX


class EnglishMorphemeFilter(BaseCandidateMorphemeFilter):
    def __init__(self) -> None:
        self._regex = re.compile(rf"({ENGLISH_REGEX}|{NUMBER_REGEX})+")

    def inscope(self, morpheme: Morpheme) -> bool:
        morpheme_str = str(morpheme)
        return morpheme.lang == "en" and (
            self._regex.fullmatch(morpheme_str) is not None or morpheme_str == "-"
        )

    def is_partof_candidate(self, morphemes: List[Morpheme], idx: int) -> bool:
        scoped_morpheme = morphemes[idx]
        num_morphemes = len(morphemes)

        if scoped_morpheme.pos in {"NOUN", "PROPN", "NUM"}:
            return True
        elif scoped_morpheme.pos == "ADJ":
            return (
                idx < num_morphemes - 1
                and morphemes[idx + 1].pos in {"NOUN", "PROPN", "ADJ", "VERB", "SYM"}
                # No line break
            )
        elif scoped_morpheme.pos == "VERB":
            return scoped_morpheme.category == "VBG" or (
                scoped_morpheme.category == "VBN"
                and idx < num_morphemes - 1
                and morphemes[idx + 1].pos in {"NOUN", "PROPN", "ADJ", "VERB", "SYM"}
            )
        elif scoped_morpheme.pos == "ADP":
            return scoped_morpheme.category == "IN"
        elif scoped_morpheme.pos == "SYM":
            return (
                scoped_morpheme.surface_form == "-"
                and 0 < idx < num_morphemes - 1
                and self._regex.match(str(morphemes[idx - 1])) is not None
                and self._regex.match(str(morphemes[idx + 1])) is not None
            )

        return False
