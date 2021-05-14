from dataclasses import dataclass
from typing import List, Dict, Any

from py_slides_term.share.data import ScoredTerm


@dataclass(frozen=True)
class PageTechnicalTermList:
    page_num: int
    terms: List[ScoredTerm]

    def to_json(self) -> Dict[str, Any]:
        return {
            "page_num": self.page_num,
            "terms": list(map(lambda term: term.to_json(), self.terms)),
        }

    @classmethod
    def from_json(cls, obj: Dict[str, Any]):
        page_num, terms = obj["page_num"], obj["terms"]
        return cls(page_num, list(map(lambda item: ScoredTerm.from_json(item), terms)))


@dataclass
class PDFTechnicalTermList:
    pdf_path: str
    pages: List[PageTechnicalTermList]

    def to_json(self) -> Dict[str, Any]:
        return {
            "pdf_path": self.pdf_path,
            "pages": list(map(lambda page: page.to_json(), self.pages)),
        }

    @classmethod
    def from_json(cls, obj: Dict[str, Any]):
        pdf_path, pages = obj["pdf_path"], obj["pages"]
        return cls(
            pdf_path,
            list(map(lambda item: PageTechnicalTermList.from_json(item), pages)),
        )


@dataclass(frozen=True)
class DomainTechnicalTermList:
    domain: str
    pdfs: List[PDFTechnicalTermList]

    def to_json(self) -> Dict[str, Any]:
        return {
            "domain": self.domain,
            "pdfs": list(map(lambda pdf: pdf.to_json(), self.pdfs)),
        }

    @classmethod
    def from_json(cls, obj: Dict[str, Any]):
        domain, pdfs = obj["domain"], obj["pdfs"]
        return cls(
            domain,
            list(map(lambda item: PDFTechnicalTermList.from_json(item), pdfs)),
        )
