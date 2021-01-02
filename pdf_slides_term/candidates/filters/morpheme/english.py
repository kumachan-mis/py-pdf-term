import re

from .base import BaseCandidateMorphemeFilter
from pdf_slides_term.mecab import BaseMeCabMorpheme


class EnglishMorphemeFilter(BaseCandidateMorphemeFilter):
    def __init__(self):
        pass

    def inscope(self, morpheme: BaseMeCabMorpheme) -> bool:
        regex = re.compile(r"[A-Za-z]+|\-")
        return regex.fullmatch(str(morpheme)) is not None

    def is_partof_candidate(self, scoped_morpheme: BaseMeCabMorpheme) -> bool:
        # TODO: use English dictionary
        return True
