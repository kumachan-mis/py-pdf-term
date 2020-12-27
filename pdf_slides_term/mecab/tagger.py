import re
import MeCab
from typing import List, Callable
from pdf_slides_term.mecab.morphemes import BaseMeCabMorpheme, MeCabMorphemeIPADic
from pdf_slides_term.share.consts import SYMBOL_REGEX


class MeCabTagger:
    # public
    def __init__(self, *args):
        self._inner_tagger = MeCab.Tagger(" ".join(args))

    def parse(
        self,
        text: str,
        mecab_morpheme_cls: Callable[[str], BaseMeCabMorpheme] = MeCabMorphemeIPADic,
        terminal: str = "EOS",
    ) -> List[BaseMeCabMorpheme]:
        if not text:
            return []

        mecab_lines = self._inner_tagger.parse(text).split("\n")
        mecab_lines = mecab_lines[: mecab_lines.index(terminal)]
        return list(
            map(
                lambda line: self._create_mecab_morpheme(mecab_morpheme_cls, line),
                mecab_lines,
            )
        )

    # private
    def _create_mecab_morpheme(
        self,
        mecab_morpheme_cls: Callable[[str], BaseMeCabMorpheme],
        mecab_line: str,
    ) -> BaseMeCabMorpheme:
        surface_form, csv_attrs = mecab_line.split("\t")
        if re.compile(rf"{SYMBOL_REGEX}+").fullmatch(surface_form):
            attrs = ["記号", "一般"]
            # c.f. https://github.com/taku910/mecab/pull/37
        else:
            attrs = csv_attrs.split(",")

        num_attrs = len(attrs)
        if num_attrs < mecab_morpheme_cls.NUM_ATTR - 1:
            attrs.extend(["*"] * (mecab_morpheme_cls.NUM_ATTR - num_attrs - 1))
        elif num_attrs > mecab_morpheme_cls.NUM_ATTR - 1:
            attrs = attrs[: mecab_morpheme_cls.NUM_ATTR - 1]

        return mecab_morpheme_cls(surface_form, *attrs)
