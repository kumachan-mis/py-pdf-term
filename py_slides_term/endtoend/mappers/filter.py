from typing import Dict, Optional, Union, Type

from py_slides_term.candidates.filters import (
    BaseCandidateMorphemeFilter,
    BaseCandidateTermFilter,
    JapaneseMorphemeFilter,
    EnglishMorphemeFilter,
    ConcatenationFilter,
    SymbolLikeFilter,
    ProperNounFilter,
)


class CandidateFilterMapper:
    def __init__(self):
        self._morpheme_filter_clses: Dict[
            str, Type[BaseCandidateMorphemeFilter]
        ] = dict()
        self._term_filter_clses: Dict[str, Type[BaseCandidateTermFilter]] = dict()

    def add_morpheme_filter_cls(
        self,
        filter_cls: Type[BaseCandidateMorphemeFilter],
        name: Optional[str] = None,
    ):
        if name is None:
            name = f"{filter_cls.__module__}.{filter_cls.__name__}"

        self._morpheme_filter_clses[name] = filter_cls

    def add_term_filter_cls(
        self,
        filter_cls: Type[BaseCandidateTermFilter],
        name: Optional[str] = None,
    ):
        if name is None:
            name = f"{filter_cls.__module__}.{filter_cls.__name__}"

        self._term_filter_clses[name] = filter_cls

    def find_morpheme_filter_cls(
        self, name: str
    ) -> Union[Type[BaseCandidateMorphemeFilter], None]:
        return self._morpheme_filter_clses.get(name)

    def find_term_filter_cls(
        self, name: str
    ) -> Union[Type[BaseCandidateTermFilter], None]:
        return self._term_filter_clses.get(name)

    @classmethod
    def default_mapper(cls):
        default = cls()

        default.add_morpheme_filter_cls(JapaneseMorphemeFilter)
        default.add_morpheme_filter_cls(EnglishMorphemeFilter)

        default.add_term_filter_cls(ConcatenationFilter)
        default.add_term_filter_cls(SymbolLikeFilter)
        default.add_term_filter_cls(ProperNounFilter)

        return default
