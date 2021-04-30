from ..base import BaseJapaneseCandidateTermFilter
from py_slides_term.share.data import Term


class JapaneseNumericFilter(BaseJapaneseCandidateTermFilter):
    # public
    def __init__(self):
        pass

    def is_candidate(self, scoped_term: Term) -> bool:
        return True
