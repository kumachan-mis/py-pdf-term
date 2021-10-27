from dataclasses import asdict, dataclass
from typing import Any, Dict, List

from py_pdf_term._common.data import ScoredTerm


@dataclass(frozen=True)
class PageStylingScoreList:
    page_num: int
    ranking: List[ScoredTerm]
    # list of pairs of lemmatized term and styling score
    # the list is sorted by the score in descending order

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> "PageStylingScoreList":
        page_num, ranking = obj["page_num"], obj["ranking"]
        return cls(
            page_num,
            list(map(lambda item: ScoredTerm.from_dict(item), ranking)),
        )


@dataclass(frozen=True)
class PDFStylingScoreList:
    pdf_path: str
    pages: List[PageStylingScoreList]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pdf_path": self.pdf_path,
            "pages": list(map(lambda page: page.to_dict(), self.pages)),
        }

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> "PDFStylingScoreList":
        pdf_path, pages = obj["pdf_path"], obj["pages"]
        return cls(
            pdf_path,
            list(map(lambda item: PageStylingScoreList.from_dict(item), pages)),
        )


@dataclass(frozen=True)
class DomainStylingScoreList:
    domain: str
    pdfs: List[PDFStylingScoreList]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "domain": self.domain,
            "pdfs": list(map(lambda pdf: pdf.to_dict(), self.pdfs)),
        }

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> "DomainStylingScoreList":
        domain, pdfs = obj["domain"], obj["pdfs"]
        return cls(
            domain,
            list(map(lambda item: PDFStylingScoreList.from_dict(item), pdfs)),
        )
