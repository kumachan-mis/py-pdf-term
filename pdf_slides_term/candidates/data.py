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
class XMLCandidateTermList:
    xml_path: str
    pages: List[PageCandidateTermList]

    def to_json(self) -> Dict:
        return {
            "xml_path": self.xml_path,
            "pages": list(map(lambda page: page.to_json(), self.pages)),
        }


@dataclass
class DomainCandidateTermList:
    domain: str
    xmls: List[XMLCandidateTermList]

    def to_json(self) -> Dict:
        return {
            "domain": self.domain,
            "xmls": list(map(lambda xml: xml.to_json(), self.xmls)),
        }
