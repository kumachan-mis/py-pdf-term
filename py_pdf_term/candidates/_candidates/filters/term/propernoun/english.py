from py_pdf_term.tokenizers import Term

from ..base import BaseEnglishCandidateTermFilter


class EnglishProperNounFilter(BaseEnglishCandidateTermFilter):
    """Term filter to remove English proper nouns from candidate terms."""

    def __init__(self) -> None:
        pass

    def is_candidate(self, scoped_term: Term) -> bool:
        return True
