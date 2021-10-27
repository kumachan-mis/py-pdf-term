from dataclasses import dataclass
from typing import Any, Dict, List

from py_pdf_term._common.data import ScoredTerm


@dataclass(frozen=True)
class PageTechnicalTermList:
    page_num: int
    terms: List[ScoredTerm]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "page_num": self.page_num,
            "terms": list(map(lambda term: term.to_dict(), self.terms)),
        }

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> "PageTechnicalTermList":
        page_num, terms = obj["page_num"], obj["terms"]
        return cls(page_num, list(map(lambda item: ScoredTerm.from_dict(item), terms)))


@dataclass(frozen=True)
class PDFTechnicalTermList:
    pdf_path: str
    pages: List[PageTechnicalTermList]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pdf_path": self.pdf_path,
            "pages": list(map(lambda page: page.to_dict(), self.pages)),
        }

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> "PDFTechnicalTermList":
        pdf_path, pages = obj["pdf_path"], obj["pages"]
        return cls(
            pdf_path,
            list(map(lambda item: PageTechnicalTermList.from_dict(item), pages)),
        )


@dataclass(frozen=True)
class DomainTechnicalTermList:
    domain: str
    pdfs: List[PDFTechnicalTermList]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "domain": self.domain,
            "pdfs": list(map(lambda pdf: pdf.to_dict(), self.pdfs)),
        }

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> "DomainTechnicalTermList":
        domain, pdfs = obj["domain"], obj["pdfs"]
        return cls(
            domain,
            list(map(lambda item: PDFTechnicalTermList.from_dict(item), pdfs)),
        )
