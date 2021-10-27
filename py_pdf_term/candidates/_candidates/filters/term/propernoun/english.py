from py_pdf_term._common.data import Term

from ..base import BaseEnglishCandidateTermFilter


class EnglishProperNounFilter(BaseEnglishCandidateTermFilter):
    def __init__(self) -> None:
        pass

    def is_candidate(self, scoped_term: Term) -> bool:
        return True
