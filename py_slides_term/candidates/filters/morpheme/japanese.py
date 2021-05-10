import re
from typing import List

from .base import BaseCandidateMorphemeFilter
from py_slides_term.tokenizer import BaseMorpheme, JapaneseMorphemeClassifier
from py_slides_term.share.consts import JAPANESE_REGEX, ALPHABET_REGEX


class JapaneseMorphemeFilter(BaseCandidateMorphemeFilter):
    # public
    def __init__(self):
        self._classifier = JapaneseMorphemeClassifier()

    def inscope(self, morpheme: BaseMorpheme) -> bool:
        regex = re.compile(rf"{JAPANESE_REGEX}+|{ALPHABET_REGEX}+|\-")
        return morpheme.lang == "ja" and regex.fullmatch(str(morpheme)) is not None

    def is_partof_candidate(self, morphemes: List[BaseMorpheme], idx: int) -> bool:
        scoped_morpheme = morphemes[idx]

        if scoped_morpheme.pos == "名詞":
            if scoped_morpheme.category == "普通名詞":
                return scoped_morpheme.subcategory in {
                    "一般",
                    "サ変可能",
                    "形状詞可能",
                    "サ変形状詞可能",
                } or (
                    scoped_morpheme.subcategory == "助数詞可能"
                    and idx > 0
                    and morphemes[idx - 1].pos == "名詞"
                    and morphemes[idx - 1].category != "数詞"
                )
            elif scoped_morpheme.category == "固有名詞":
                return True
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
                and scoped_morpheme.subcategory in {"一般", "サ変可能", "形状詞可能"}
            )
        elif scoped_morpheme.pos == "助詞":
            return self._classifier.is_modifying_particle(scoped_morpheme)
        elif scoped_morpheme.pos == "補助記号":
            scoped_morpheme_str = str(scoped_morpheme)
            regex = re.compile(rf"{JAPANESE_REGEX}+")
            if scoped_morpheme_str == "-":
                return (
                    0 < idx < len(morphemes) - 1
                    and regex.match(str(morphemes[idx - 1])) is None
                    and regex.match(str(morphemes[idx + 1])) is None
                )
            elif scoped_morpheme_str == "・":
                return (
                    0 < idx < len(morphemes) - 1
                    and regex.match(str(morphemes[idx - 1])) is not None
                    and regex.match(str(morphemes[idx + 1])) is not None
                )

        return False
