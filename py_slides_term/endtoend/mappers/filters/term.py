from typing import Type

from ..base import BaseMapper
from ..consts import PACKAGE_NAME
from py_slides_term.candidates import (
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


class CandidateTermFilterMapper(BaseMapper[Type[BaseCandidateTermFilter]]):
    @classmethod
    def default_mapper(cls):
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
