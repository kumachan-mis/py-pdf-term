from typing import Self

from py_pdf_term._common.consts import PACKAGE_NAME
from py_pdf_term.tokenizers import (
    BaseLanguageTokenizer,
    EnglishTokenizer,
    JapaneseTokenizer,
)

from ..base import BaseMapper


class LanguageTokenizerMapper(BaseMapper[type[BaseLanguageTokenizer]]):
    """Mapper to find language tokenizer classes."""

    @classmethod
    def default_mapper(cls) -> Self:
        default_mapper = cls()

        lang_tokenizer_clses: list[type[BaseLanguageTokenizer]] = [
            JapaneseTokenizer,
            EnglishTokenizer,
        ]
        for lang_tokenizer_cls in lang_tokenizer_clses:
            default_mapper.add(
                f"{PACKAGE_NAME}.{lang_tokenizer_cls.__name__}", lang_tokenizer_cls
            )

        return default_mapper
