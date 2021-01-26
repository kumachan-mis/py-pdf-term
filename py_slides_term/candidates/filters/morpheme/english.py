import re
from typing import List

from .base import BaseCandidateMorphemeFilter
from py_slides_term.morphemes import BaseMorpheme


class EnglishMorphemeFilter(BaseCandidateMorphemeFilter):
    def __init__(self):
        pass

    def inscope(self, morpheme: BaseMorpheme) -> bool:
        regex = re.compile(r"[A-Za-z]+|\-")
        return regex.fullmatch(str(morpheme)) is not None

    def is_partof_candidate(self, morphemes: List[BaseMorpheme], idx: int) -> bool:
        scoped_morpheme = morphemes[idx]

        if scoped_morpheme.pos == "NOUN":
            return True
        elif scoped_morpheme.pos == "PROPN":
            return True
        elif scoped_morpheme.pos == "ADJ":
            return True
        elif scoped_morpheme.pos == "VERB":
            return scoped_morpheme.category in {"VBG", "VBN"}
        elif scoped_morpheme.pos == "ADP":
            return scoped_morpheme.category == "IN"
        elif scoped_morpheme.pos == "PUNCT":
            return scoped_morpheme.category == "HYPH" and 0 < idx < len(morphemes) - 1

        return False
