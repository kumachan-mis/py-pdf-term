from typing import Self

from py_pdf_term._common.consts import PACKAGE_NAME
from py_pdf_term.candidates.filters import (
    BaseCandidateTermFilter,
    BaseCandidateTokenFilter,
    EnglishConcatenationFilter,
    EnglishNumericFilter,
    EnglishProperNounFilter,
    EnglishSymbolLikeFilter,
    EnglishTokenFilter,
    JapaneseConcatenationFilter,
    JapaneseNumericFilter,
    JapaneseProperNounFilter,
    JapaneseSymbolLikeFilter,
    JapaneseTokenFilter,
)

from ..base import BaseMapper


class CandidateTokenFilterMapper(BaseMapper[type[BaseCandidateTokenFilter]]):
    """Mapper to find candidate token filter classes."""

    @classmethod
    def default_mapper(cls) -> Self:
        default_mapper = cls()

        token_filter_clses: list[type[BaseCandidateTokenFilter]] = [
            JapaneseTokenFilter,
            EnglishTokenFilter,
        ]
        for filter_cls in token_filter_clses:
            default_mapper.add(f"{PACKAGE_NAME}.{filter_cls.__name__}", filter_cls)

        return default_mapper


class CandidateTermFilterMapper(BaseMapper[type[BaseCandidateTermFilter]]):
    """Mapper to find candidate term filter classes."""

    @classmethod
    def default_mapper(cls) -> Self:
        default_mapper = cls()

        term_filter_clses: list[type[BaseCandidateTermFilter]] = [
            JapaneseConcatenationFilter,
            EnglishConcatenationFilter,
            JapaneseSymbolLikeFilter,
            EnglishSymbolLikeFilter,
            JapaneseProperNounFilter,
            EnglishProperNounFilter,
            JapaneseNumericFilter,
            EnglishNumericFilter,
        ]
        for filter_cls in term_filter_clses:
            default_mapper.add(f"{PACKAGE_NAME}.{filter_cls.__name__}", filter_cls)

        return default_mapper
