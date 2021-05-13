from dataclasses import dataclass, asdict
from typing import Dict, List, Any

from py_slides_term.share.data import ScoredTerm


@dataclass(frozen=True)
class PageStylingScoreList:
    page_num: int
    ranking: List[ScoredTerm]

    def to_json(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_json(cls, obj: Dict[str, Any]):
        return cls(**obj)


@dataclass(frozen=True)
class PDFStylingScoreList:
    pdf_path: str
    pages: List[PageStylingScoreList]

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
            list(map(lambda item: PageStylingScoreList.from_json(item), pages)),
        )


@dataclass(frozen=True)
class DomainStylingScoreList:
    domain: str
    pdfs: List[PDFStylingScoreList]

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
            list(map(lambda item: PDFStylingScoreList.from_json(item), pdfs)),
        )
