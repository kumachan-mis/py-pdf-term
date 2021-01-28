from typing import Type

from ..base import BaseMapper
from py_slides_term.candidates import (
    BaseCandidateTermFilter,
    JapaneseConcatenationFilter,
    EnglishConcatenationFilter,
    JapaneseSymbolLikeFilter,
    EnglishSymbolLikeFilter,
    JapaneseProperNounFilter,
    EnglishProperNounFilter,
)


class CandidateTermFilterMapper(BaseMapper[Type[BaseCandidateTermFilter]]):
    @classmethod
    def default_mapper(cls):
        module_path = "py_slides_term.candidates"
        default_mapper = cls()

        term_filter_clses = [
            JapaneseConcatenationFilter,
            EnglishConcatenationFilter,
            JapaneseSymbolLikeFilter,
            EnglishSymbolLikeFilter,
            JapaneseProperNounFilter,
            EnglishProperNounFilter,
        ]
        for filter_cls in term_filter_clses:
            default_mapper.add(f"{module_path}.{filter_cls.__name__}", filter_cls)

        return default_mapper
