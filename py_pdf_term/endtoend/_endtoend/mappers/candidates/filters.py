from typing import Type

from ..base import BaseMapper
from ..consts import PACKAGE_NAME
from py_pdf_term.candidates.filters import (
    BaseCandidateMorphemeFilter,
    JapaneseMorphemeFilter,
    EnglishMorphemeFilter,
    BaseCandidateTermFilter,
    JapaneseConcatenationFilter,
    EnglishConcatenationFilter,
    JapaneseSymbolLikeFilter,
    EnglishSymbolLikeFilter,
    JapaneseProperNounFilter,
    EnglishProperNounFilter,
    JapaneseNumericFilter,
    EnglishNumericFilter,
)


class CandidateMorphemeFilterMapper(BaseMapper[Type[BaseCandidateMorphemeFilter]]):
    @classmethod
    def default_mapper(cls) -> "CandidateMorphemeFilterMapper":
        default_mapper = cls()

        morpheme_filter_clses = [JapaneseMorphemeFilter, EnglishMorphemeFilter]
        for filter_cls in morpheme_filter_clses:
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
