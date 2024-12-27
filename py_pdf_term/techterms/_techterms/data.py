from dataclasses import dataclass
from typing import Any, Self

from py_pdf_term._common.data import ScoredTerm


@dataclass(frozen=True)
class PageTechnicalTermList:
    """Page number and technical terms of the page.

    Args
    ----
        page_num:
            Page number of a PDF file.
        terms:
            Technical terms of the page.
    """

    page_num: int
    terms: list[ScoredTerm]

    def to_dict(self) -> dict[str, Any]:
        return {
            "page_num": self.page_num,
            "terms": list(map(lambda term: term.to_dict(), self.terms)),
        }

    @classmethod
    def from_dict(cls, obj: dict[str, Any]) -> Self:
        page_num, terms = obj["page_num"], obj["terms"]
        return cls(page_num, list(map(lambda item: ScoredTerm.from_dict(item), terms)))


@dataclass(frozen=True)
class PDFTechnicalTermList:
    """Path of a PDF file and technical terms of the PDF file.

    Args
    ----
        pdf_path:
            Path of a PDF file.
        pages:
            Technical terms of each page of the PDF file.
    """

    pdf_path: str
    pages: list[PageTechnicalTermList]

    def to_dict(self) -> dict[str, Any]:
        return {
            "pdf_path": self.pdf_path,
            "pages": list(map(lambda page: page.to_dict(), self.pages)),
        }

    @classmethod
    def from_dict(cls, obj: dict[str, Any]) -> Self:
        pdf_path, pages = obj["pdf_path"], obj["pages"]
        return cls(
            pdf_path,
            list(map(lambda item: PageTechnicalTermList.from_dict(item), pages)),
        )


@dataclass(frozen=True)
class DomainTechnicalTermList:
    """Domain name of PDF files and technical terms of the domain.

    Args
    ----
        domain:
            Domain name. (e.g., "natural language processing")
        pdfs:
            Technical terms of each PDF file of the domain.
    """

    domain: str
    pdfs: list[PDFTechnicalTermList]

    def to_dict(self) -> dict[str, Any]:
        return {
            "domain": self.domain,
            "pdfs": list(map(lambda pdf: pdf.to_dict(), self.pdfs)),
        }

    @classmethod
    def from_dict(cls, obj: dict[str, Any]) -> Self:
        domain, pdfs = obj["domain"], obj["pdfs"]
        return cls(
            domain,
            list(map(lambda item: PDFTechnicalTermList.from_dict(item), pdfs)),
        )
