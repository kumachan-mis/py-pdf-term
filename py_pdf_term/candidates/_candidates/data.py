from dataclasses import dataclass
from typing import Any, Callable, Self

from py_pdf_term.tokenizers import Term


@dataclass(frozen=True)
class PageCandidateTermList:
    """Page number and candidate terms of the page.

    Args
    ----
        page_num:
            Page number of a PDF file.
        candidates:
            Candidate terms of the page.
    """

    page_num: int
    candidates: list[Term]

    def to_nostyle_candidates_dict(
        self, to_str: Callable[[Term], str] = str
    ) -> dict[str, Term]:
        term_dict: dict[str, Term] = dict()
        for candidate in self.candidates:
            candidate_str = to_str(candidate)
            if candidate_str in term_dict:
                continue
            term_dict[candidate_str] = Term(candidate.tokens, 0.0, "", False)
        return term_dict

    def to_candidates_str_set(self, to_str: Callable[[Term], str] = str) -> set[str]:
        return {to_str(candidate) for candidate in self.candidates}

    def to_dict(self) -> dict[str, Any]:
        return {
            "page_num": self.page_num,
            "candidates": list(map(lambda term: term.to_dict(), self.candidates)),
        }

    @classmethod
    def from_dict(cls, obj: dict[str, Any]) -> Self:
        page_num, candidates = obj["page_num"], obj["candidates"]
        return cls(
            page_num,
            list(map(lambda item: Term.from_dict(item), candidates)),
        )


@dataclass(frozen=True)
class PDFCandidateTermList:
    """Path of a PDF file and candidate terms of the PDF file.

    Args
    ----
        pdf_path:
            Path of a PDF file.
        pages:
            Candidate terms of each page of the PDF file.
    """

    pdf_path: str
    pages: list[PageCandidateTermList]

    def to_nostyle_candidates_dict(
        self, to_str: Callable[[Term], str] = str
    ) -> dict[str, Term]:
        term_dict: dict[str, Term] = dict()
        for page in self.pages:
            candidate_items = page.to_nostyle_candidates_dict(to_str).items()
            for candidate_str, candidate in candidate_items:
                if candidate_str in term_dict:
                    continue
                term_dict[candidate_str] = candidate
        return term_dict

    def to_candidates_str_set(self, to_str: Callable[[Term], str] = str) -> set[str]:
        empty: set[str] = set()
        return empty.union(
            *map(lambda page: page.to_candidates_str_set(to_str), self.pages)
        )

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
            list(map(lambda item: PageCandidateTermList.from_dict(item), pages)),
        )


@dataclass(frozen=True)
class DomainCandidateTermList:
    """Domain name of PDF files and candidate terms of the domain.

    Args
    ----
        domain:
            Domain name. (e.g., "natural language processing")
        pdfs:
            Candidate terms of each PDF file of the domain.
    """

    domain: str
    pdfs: list[PDFCandidateTermList]

    def to_nostyle_candidates_dict(
        self, to_str: Callable[[Term], str] = str
    ) -> dict[str, Term]:
        term_dict: dict[str, Term] = dict()
        for pdf in self.pdfs:
            candidate_items = pdf.to_nostyle_candidates_dict(to_str).items()
            for candidate_str, candidate in candidate_items:
                if candidate_str in term_dict:
                    continue
                term_dict[candidate_str] = candidate
        return term_dict

    def to_candidates_str_set(self, to_str: Callable[[Term], str] = str) -> set[str]:
        empty: set[str] = set()
        return empty.union(
            *map(lambda pdf: pdf.to_candidates_str_set(to_str), self.pdfs)
        )

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
            list(map(lambda item: PDFCandidateTermList.from_dict(item), pdfs)),
        )
