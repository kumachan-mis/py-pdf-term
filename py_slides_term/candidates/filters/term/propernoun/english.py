from ..base import BaseEnglishCandidateTermFilter
from py_slides_term.share.data import Term


class EnglishProperNounFilter(BaseEnglishCandidateTermFilter):
    def __init__(self):
        pass

    def is_candidate(self, scoped_term: Term) -> bool:
        return True
