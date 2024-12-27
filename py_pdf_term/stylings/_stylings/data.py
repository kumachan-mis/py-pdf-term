from dataclasses import asdict, dataclass
from typing import Any, Self

from py_pdf_term._common.data import ScoredTerm


@dataclass(frozen=True)
class PageStylingScoreList:
    """Page number and styling scores of technical terms of the page.

    Args
    ----
        page_num:
            Page number of a PDF file.
        ranking:
            List of pairs of lemmatized term and styling score.
            The list is sorted by the score in descending order.
    """

    page_num: int
    ranking: list[ScoredTerm]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, obj: dict[str, Any]) -> Self:
        page_num, ranking = obj["page_num"], obj["ranking"]
        return cls(
            page_num,
            list(map(lambda item: ScoredTerm.from_dict(item), ranking)),
        )


@dataclass(frozen=True)
class PDFStylingScoreList:
    """Path of a PDF file and styling scores of technical terms of the PDF file.

    Args
    ----
        pdf_path:
            Path of a PDF file.
        pages:
            Styling scores of each page of the PDF file.
    """

    pdf_path: str
    pages: list[PageStylingScoreList]

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
            list(map(lambda item: PageStylingScoreList.from_dict(item), pages)),
        )


@dataclass(frozen=True)
class DomainStylingScoreList:
    """Domain name of PDF files and styling scores of technical terms of the domain.

    Args
    ----
        domain:
            Domain name. (e.g., "natural language processing")
        pdfs:
            Styling scores of each PDF file of the domain.
    """

    domain: str
    pdfs: list[PDFStylingScoreList]

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
            list(map(lambda item: PDFStylingScoreList.from_dict(item), pdfs)),
        )
