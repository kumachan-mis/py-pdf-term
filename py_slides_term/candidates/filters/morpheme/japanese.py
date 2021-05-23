import re
from typing import List

from .base import BaseCandidateMorphemeFilter
from py_slides_term.tokenizer import Morpheme, JapaneseMorphemeClassifier
from py_slides_term.share.consts import JAPANESE_REGEX, ENGLISH_REGEX, NUMBER_REGEX


class JapaneseMorphemeFilter(BaseCandidateMorphemeFilter):
    def __init__(self):
        self._regex = re.compile(rf"({JAPANESE_REGEX}|{ENGLISH_REGEX}|{NUMBER_REGEX})+")
        self._classifier = JapaneseMorphemeClassifier()

    def inscope(self, morpheme: Morpheme) -> bool:
        morpheme_str = str(morpheme)
        return morpheme.lang == "ja" and (
            self._regex.fullmatch(morpheme_str) is not None or morpheme_str == "-"
        )

    def is_partof_candidate(self, morphemes: List[Morpheme], idx: int) -> bool:
        scoped_morpheme = morphemes[idx]

        if scoped_morpheme.pos == "名詞":
            return (
                (
                    scoped_morpheme.category == "普通名詞"
                    and scoped_morpheme.subcategory
                    in {"一般", "サ変可能", "形状詞可能", "サ変形状詞可能", "助数詞可能"}
                )
                or scoped_morpheme.category == "固有名詞"
                or scoped_morpheme.category == "数詞"
            )
        elif scoped_morpheme.pos == "形状詞":
            return scoped_morpheme.category in {"一般"}
        elif scoped_morpheme.pos == "動詞":
            return scoped_morpheme.category in {"一般"}
        elif scoped_morpheme.pos == "形容詞":
            return scoped_morpheme.category in {"一般"}
        elif scoped_morpheme.pos == "接頭辞":
            return True
        elif scoped_morpheme.pos == "接尾辞":
            return (
                scoped_morpheme.category == "名詞的"
                and scoped_morpheme.subcategory in {"一般", "サ変可能", "形状詞可能", "助数詞"}
            )
        elif scoped_morpheme.pos == "助詞":
            return self._classifier.is_modifying_particle(scoped_morpheme)
        elif scoped_morpheme.pos == "記号":
            return self._regex.match(str(scoped_morpheme)) is not None
        elif scoped_morpheme.pos == "補助記号":
            scoped_morpheme_str = str(scoped_morpheme)
            if scoped_morpheme_str == "-":
                return (
                    0 < idx < len(morphemes) - 1
                    and self._regex.match(str(morphemes[idx - 1])) is not None
                    and self._regex.match(str(morphemes[idx + 1])) is not None
                )
            elif scoped_morpheme_str == "・":
                return (
                    0 < idx < len(morphemes) - 1
                    and self._regex.match(str(morphemes[idx - 1])) is not None
                    and self._regex.match(str(morphemes[idx + 1])) is not None
                )

        return False
