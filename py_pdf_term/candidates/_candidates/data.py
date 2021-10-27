from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Set

from py_pdf_term._common.data import Term


@dataclass(frozen=True)
class PageCandidateTermList:
    page_num: int
    candidates: List[Term]

    def to_nostyle_candidates_dict(
        self, to_str: Callable[[Term], str] = str
    ) -> Dict[str, Term]:
        term_dict: Dict[str, Term] = dict()
        for candidate in self.candidates:
            candidate_str = to_str(candidate)
            if candidate_str in term_dict:
                continue
            term_dict[candidate_str] = Term(candidate.tokens, 0.0, "", False)
        return term_dict

    def to_candidates_str_set(self, to_str: Callable[[Term], str] = str) -> Set[str]:
        return {to_str(candidate) for candidate in self.candidates}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "page_num": self.page_num,
            "candidates": list(map(lambda term: term.to_dict(), self.candidates)),
        }

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> "PageCandidateTermList":
        page_num, candidates = obj["page_num"], obj["candidates"]
        return cls(
            page_num,
            list(map(lambda item: Term.from_dict(item), candidates)),
        )


@dataclass(frozen=True)
class PDFCandidateTermList:
    pdf_path: str
    pages: List[PageCandidateTermList]

    def to_nostyle_candidates_dict(
        self, to_str: Callable[[Term], str] = str
    ) -> Dict[str, Term]:
        term_dict: Dict[str, Term] = dict()
        for page in self.pages:
            candidate_items = page.to_nostyle_candidates_dict(to_str).items()
            for candidate_str, candidate in candidate_items:
                if candidate_str in term_dict:
                    continue
                term_dict[candidate_str] = candidate
        return term_dict

    def to_candidates_str_set(self, to_str: Callable[[Term], str] = str) -> Set[str]:
        empty: Set[str] = set()
        return empty.union(
            *map(lambda page: page.to_candidates_str_set(to_str), self.pages)
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pdf_path": self.pdf_path,
            "pages": list(map(lambda page: page.to_dict(), self.pages)),
        }

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> "PDFCandidateTermList":
        pdf_path, pages = obj["pdf_path"], obj["pages"]
        return cls(
            pdf_path,
            list(map(lambda item: PageCandidateTermList.from_dict(item), pages)),
        )


@dataclass(frozen=True)
class DomainCandidateTermList:
    domain: str
    pdfs: List[PDFCandidateTermList]

    def to_nostyle_candidates_dict(
        self, to_str: Callable[[Term], str] = str
    ) -> Dict[str, Term]:
        term_dict: Dict[str, Term] = dict()
        for pdf in self.pdfs:
            candidate_items = pdf.to_nostyle_candidates_dict(to_str).items()
            for candidate_str, candidate in candidate_items:
                if candidate_str in term_dict:
                    continue
                term_dict[candidate_str] = candidate
        return term_dict

    def to_candidates_str_set(self, to_str: Callable[[Term], str] = str) -> Set[str]:
        empty: Set[str] = set()
        return empty.union(
            *map(lambda pdf: pdf.to_candidates_str_set(to_str), self.pdfs)
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "domain": self.domain,
            "pdfs": list(map(lambda pdf: pdf.to_dict(), self.pdfs)),
        }

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> "DomainCandidateTermList":
        domain, pdfs = obj["domain"], obj["pdfs"]
        return cls(
            domain,
            list(map(lambda item: PDFCandidateTermList.from_dict(item), pdfs)),
        )
