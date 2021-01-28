from typing import List

from ..filters import CandidateFilter
from py_slides_term.share.data import Term


class RepeatSplitter:
    # public
    def __init__(self, candidate_filter: CandidateFilter):
        self._filter = candidate_filter

    def split(self, term: Term) -> List[Term]:
        return [term]
