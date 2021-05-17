from dataclasses import dataclass
from typing import List, Set, Dict, Any, Type

from py_slides_term.tokenizer import BaseMorpheme, SpaCyMorpheme
from py_slides_term.share.data import Term


@dataclass(frozen=True)
class PageCandidateTermList:
    page_num: int
    candidates: List[Term]

    def to_nostyle_term_dict(self) -> Dict[str, Term]:
        return {
            str(candidate): Term(candidate.morphemes, 0.0, "", False)
            for candidate in self.candidates
        }

    def to_term_str_set(self) -> Set[str]:
        return {str(candidate) for candidate in self.candidates}

    def to_json(self) -> Dict[str, Any]:
        return {
            "page_num": self.page_num,
            "candidates": list(map(lambda term: term.to_json(), self.candidates)),
        }

    @classmethod
    def from_json(
        cls,
        obj: Dict[str, Any],
        morpheme_cls: Type[BaseMorpheme] = SpaCyMorpheme,
    ):
        page_num, candidates = obj["page_num"], obj["candidates"]
        return cls(
            page_num,
            list(map(lambda item: Term.from_json(item, morpheme_cls), candidates)),
        )


@dataclass(frozen=True)
class PDFCandidateTermList:
    pdf_path: str
    pages: List[PageCandidateTermList]

    def to_nostyle_term_dict(self) -> Dict[str, Term]:
        return {
            candidate_str: candidate
            for page in self.pages
            for candidate_str, candidate in page.to_nostyle_term_dict().items()
        }

    def to_term_str_set(self) -> Set[str]:
        return set[str]().union(*map(lambda page: page.to_term_str_set(), self.pages))

    def to_json(self) -> Dict[str, Any]:
        return {
            "pdf_path": self.pdf_path,
            "pages": list(map(lambda page: page.to_json(), self.pages)),
        }

    @classmethod
    def from_json(
        cls,
        obj: Dict[str, Any],
        morpheme_cls: Type[BaseMorpheme] = SpaCyMorpheme,
    ):
        pdf_path, pages = obj["pdf_path"], obj["pages"]
        return cls(
            pdf_path,
            list(
                map(
                    lambda item: PageCandidateTermList.from_json(item, morpheme_cls),
                    pages,
                )
            ),
        )


@dataclass(frozen=True)
class DomainCandidateTermList:
    domain: str
    pdfs: List[PDFCandidateTermList]

    def to_nostyle_term_dict(self) -> Dict[str, Term]:
        return {
            candidate_str: candidate
            for pdf in self.pdfs
            for candidate_str, candidate in pdf.to_nostyle_term_dict().items()
        }

    def to_term_str_set(self) -> Set[str]:
        return set[str]().union(*map(lambda pdf: pdf.to_term_str_set(), self.pdfs))

    def to_json(self) -> Dict[str, Any]:
        return {
            "domain": self.domain,
            "pdfs": list(map(lambda pdf: pdf.to_json(), self.pdfs)),
        }

    @classmethod
    def from_json(
        cls,
        obj: Dict[str, Any],
        morpheme_cls: Type[BaseMorpheme] = SpaCyMorpheme,
    ):
        domain, pdfs = obj["domain"], obj["pdfs"]
        return cls(
            domain,
            list(
                map(
                    lambda item: PDFCandidateTermList.from_json(item, morpheme_cls),
                    pdfs,
                )
            ),
        )
