import re

from pdf_slides_term.mecab.morphemes import BaseMeCabMorpheme
from pdf_slides_term.share.data import TechnicalTerm
from pdf_slides_term.share.consts import HIRAGANA_REGEX, KATAKANA_REGEX, KANJI_REGEX


class CandidateTermFilter:
    def is_part_of_candidate_term(self, morpheme: BaseMeCabMorpheme) -> bool:
        if morpheme.pos == "名詞":
            valid_categories = {"一般", "サ変接続", "固有名詞", "形容動詞語幹", "接尾"}
            return (
                morpheme.category in valid_categories
                and morpheme.subcategory not in {"助数詞"}
            )
        elif morpheme.pos == "接頭詞":
            return morpheme.category in {"名詞接続"}
        elif morpheme.pos == "動詞":
            return morpheme.category in {"自立"}
        elif morpheme.pos == "形容詞":
            return morpheme.category in {"自立"}
        else:
            return False

    def is_candidate_term(self, term: TechnicalTerm) -> bool:
        term_str = str(term)
        valid_regex = re.compile(
            rf"({HIRAGANA_REGEX}|{KATAKANA_REGEX}|{KANJI_REGEX}|[a-zA-Z])+"
        )
        invalid_regex = re.compile(rf"{HIRAGANA_REGEX}|{KATAKANA_REGEX}|[A-Z]|[a-z]+")
        if (
            valid_regex.fullmatch(term_str) is None
            or invalid_regex.fullmatch(term_str) is not None
        ):
            return False

        num_morphemes = len(term.morphemes)
        if num_morphemes == 1:
            morpheme = term.morphemes[0]
            return (
                morpheme.pos == "名詞"
                and morpheme.category in {"一般", "サ変接続", "固有名詞"}
                and morpheme.subcategory not in {"人名", "組織", "地域"}
            )

        for i in range(num_morphemes):
            morpheme = term.morphemes[i]
            if morpheme.pos not in {"動詞", "形容詞"}:
                continue

            next_morpheme = term.morphemes[i + 1] if i + 1 < num_morphemes else None
            is_valid_morpheme = (
                next_morpheme is not None
                and next_morpheme.pos == "名詞"
                and next_morpheme.category in {"接尾"}
                and next_morpheme.subcategory in {"特殊"}
            )

            if not is_valid_morpheme:
                return False

        return True
