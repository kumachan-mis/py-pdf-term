from dataclasses import dataclass
from typing import List, Dict

from pdf_slides_term.share.data import TechnicalTerm


@dataclass
class PageCandidateTermList:
    page_num: int
    candidates: List[TechnicalTerm]

    def to_json(self) -> Dict:
        return {
            "page_num": self.page_num,
            "candidates": list(map(lambda term: term.to_json(), self.candidates)),
        }


@dataclass
class CandidateTermList:
    xml_path: str
    pages: List[PageCandidateTermList]

    def to_json(self) -> Dict:
        return {
            "xml_path": self.xml_path,
            "candicate_terms": list(map(lambda page: page.to_json(), self.pages)),
        }
