from typing import Type

from ..base import BaseMapper
from ..consts import PACKAGE_NAME
from py_slides_term.candidates import (
    BaseCandidateMorphemeFilter,
    JapaneseMorphemeFilter,
    EnglishMorphemeFilter,
)


class CandidateMorphemeFilterMapper(BaseMapper[Type[BaseCandidateMorphemeFilter]]):
    @classmethod
    def default_mapper(cls):
        default_mapper = cls()

        morpheme_filter_clses = [JapaneseMorphemeFilter, EnglishMorphemeFilter]
        for filter_cls in morpheme_filter_clses:
            default_mapper.add(f"{PACKAGE_NAME}.{filter_cls.__name__}", filter_cls)

        return default_mapper
