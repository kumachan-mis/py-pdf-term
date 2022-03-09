from typing import Type

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
from ..consts import PACKAGE_NAME


class CandidateTokenFilterMapper(BaseMapper[Type[BaseCandidateTokenFilter]]):
    @classmethod
    def default_mapper(cls) -> "CandidateTokenFilterMapper":
        default_mapper = cls()

        token_filter_clses = [JapaneseTokenFilter, EnglishTokenFilter]
        for filter_cls in token_filter_clses:
            default_mapper.add(f"{PACKAGE_NAME}.{filter_cls.__name__}", filter_cls)

        return default_mapper


class CandidateTermFilterMapper(BaseMapper[Type[BaseCandidateTermFilter]]):
    @classmethod
    def default_mapper(cls) -> "CandidateTermFilterMapper":
        default_mapper = cls()

        term_filter_clses = [
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
