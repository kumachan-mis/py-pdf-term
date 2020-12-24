import re
from janome.tokenizer import Tokenizer
from typing import List, Callable
from pdf_slides_term.morphemes import BaseMorpheme, MorphemeIPADic
from pdf_slides_term.consts import SYMBOLS


class JanomeTokenizer:

    SYMBOL_REGEX = re.compile(rf"[{re.escape(SYMBOLS)}]+")

    def __init__(self, *args, **kargs):
        self._inner_tokenizer = Tokenizer(*args, **kargs)

    def tokenize(
        self,
        text: str,
        morpheme_class: Callable[[str], BaseMorpheme] = MorphemeIPADic,
    ) -> List[BaseMorpheme]:
        if not text:
            return []

        tokens = self._inner_tokenizer.tokenize(text)
        return list(
            map(
                lambda token: self._create_morpheme(morpheme_class, str(token)),
                tokens,
            )
        )

    def _create_morpheme(
        self,
        morpheme_class: Callable[[str], BaseMorpheme],
        token: str,
    ) -> BaseMorpheme:
        try:
            surface_form, csv_attrs = token.split("\t")
        except ValueError:
            surface_form, csv_attrs = "\t", "記号,空白,*,*,*,*,\t,*,*"
        if JanomeTokenizer.SYMBOL_REGEX.fullmatch(surface_form):
            attrs = ["記号", "一般"]
            # c.f. https://github.com/taku910/mecab/pull/37
        else:
            attrs = csv_attrs.split(",")

        num_attrs = len(attrs)
        if num_attrs < morpheme_class.NUM_ATTR - 1:
            attrs.extend(["*"] * (morpheme_class.NUM_ATTR - num_attrs - 1))
        elif num_attrs > morpheme_class.NUM_ATTR - 1:
            attrs = attrs[: morpheme_class.NUM_ATTR - 1]

        return morpheme_class(surface_form, *attrs)
