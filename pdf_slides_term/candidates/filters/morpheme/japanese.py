import re

from .base import BaseCandidateMorphemeFilter
from pdf_slides_term.mecab import BaseMeCabMorpheme
from pdf_slides_term.share.consts import HIRAGANA_REGEX, KATAKANA_REGEX, KANJI_REGEX


class JapaneseMorphemeFilter(BaseCandidateMorphemeFilter):
    def __init__(self):
        pass

    def inscope(self, morpheme: BaseMeCabMorpheme) -> bool:
        regex = re.compile(rf"({HIRAGANA_REGEX}|{KATAKANA_REGEX}|{KANJI_REGEX})+")
        return regex.fullmatch(str(morpheme)) is not None

    def is_partof_candidate(self, scoped_morpheme: BaseMeCabMorpheme) -> bool:
        if scoped_morpheme.pos == "名詞":
            categories = {"一般", "サ変接続", "固有名詞", "形容動詞語幹", "ナイ形容詞語幹", "接尾"}
            return (
                scoped_morpheme.category in categories
                and scoped_morpheme.subcategory not in {"助数詞"}
            )
        elif scoped_morpheme.pos == "接頭詞":
            return scoped_morpheme.category in {"名詞接続"}
        elif scoped_morpheme.pos == "動詞":
            return scoped_morpheme.category in {"自立"}
        elif scoped_morpheme.pos == "形容詞":
            return scoped_morpheme.category in {"自立"}
        elif scoped_morpheme.pos == "助詞":
            return scoped_morpheme.category in {"連体化"}
        else:
            return False
