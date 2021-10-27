from typing import Type

from py_pdf_term.tokenizer.langs import (
    BaseLanguageTokenizer,
    EnglishTokenizer,
    JapaneseTokenizer,
)

from ..base import BaseMapper
from ..consts import PACKAGE_NAME


class LanguageTokenizerMapper(BaseMapper[Type[BaseLanguageTokenizer]]):
    @classmethod
    def default_mapper(cls) -> "LanguageTokenizerMapper":
        default_mapper = cls()

        lang_tokenizer_clses = [JapaneseTokenizer, EnglishTokenizer]
        for lang_tokenizer_cls in lang_tokenizer_clses:
            default_mapper.add(
                f"{PACKAGE_NAME}.{lang_tokenizer_cls.__name__}", lang_tokenizer_cls
            )

        return default_mapper
