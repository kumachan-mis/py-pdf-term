import re
from typing import List, Iterable, Type, cast

from janome.tokenizer import Tokenizer, Token

from .data import BaseMorpheme, MorphemeIPADic
from py_slides_term.share.consts import SYMBOL_REGEX


class JanomeTokenizer:
    # public
    def __init__(self):
        self._inner_tokenizer = Tokenizer()

    def tokenize(
        self,
        text: str,
        morpheme_cls: Type[BaseMorpheme] = MorphemeIPADic,
        terminal: str = "EOS",
    ) -> List[BaseMorpheme]:
        if not text:
            return []

        text = text.replace("・", " ・ ")
        tokens = cast(Iterable[Token], self._inner_tokenizer.tokenize(text))
        return list(
            map(lambda token: self._create_morpheme(morpheme_cls, token), tokens)
        )

    # private
    def _create_morpheme(
        self, morpheme_cls: Type[BaseMorpheme], token: Token
    ) -> BaseMorpheme:
        # pyright:reportUnknownMemberType=false
        surface_form = cast(str, token.surface)
        if re.compile(rf"{SYMBOL_REGEX}+").fullmatch(surface_form):
            attrs = ["記号", "一般"]
        else:
            attrs = cast(
                List[str],
                [
                    *cast(str, token.part_of_speech).split(","),
                    token.infl_type,
                    token.infl_form,
                    token.base_form,
                    token.reading,
                    token.phonetic,
                ],
            )

        num_attrs = len(attrs)

        if num_attrs < morpheme_cls.NUM_ATTR - 1:
            attrs.extend(["*"] * (morpheme_cls.NUM_ATTR - num_attrs - 1))
        elif num_attrs > morpheme_cls.NUM_ATTR - 1:
            attrs = attrs[: morpheme_cls.NUM_ATTR - 1]

        return morpheme_cls(surface_form, *attrs)
