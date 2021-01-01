from dataclasses import dataclass, asdict
from typing import List, Set, Dict, Any, Type

from pdf_slides_term.mecab import BaseMeCabMorpheme, MeCabMorphemeIPADic
from pdf_slides_term.share.data import Term


@dataclass(frozen=True)
class PDFnXMLPath:
    pdf_path: str
    xml_path: str

    def to_json(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_json(cls, obj: Dict[str, Any]):
        return cls(**obj)


@dataclass(frozen=True)
class PDFnXMLContent:
    pdf_path: str
    xml_content: str

    def to_json(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_json(cls, obj: Dict[str, Any]):
        return cls(**obj)


@dataclass(frozen=True)
class DomainCandidateTermSet:
    domain: str
    candidates: Set[str]

    def to_json(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_json(cls, obj: Dict[str, Any]):
        return cls(**obj)


@dataclass(frozen=True)
class DomainCandidateTermDict:
    domain: str
    candidates: Dict[str, Term]

    def to_json(self) -> Dict[str, Any]:
        return {
            "domain": self.domain,
            "candidates": {
                candidate_str: candidate.to_json()
                for candidate_str, candidate in self.candidates.items()
            },
        }

    @classmethod
    def from_json(
        cls,
        obj: Dict[str, Any],
        morpheme_cls: Type[BaseMeCabMorpheme] = MeCabMorphemeIPADic,
    ):
        domain, candidates = obj["domain"], obj["candidates"]
        return cls(
            domain,
            {
                candidate_str: Term.from_json(candidate, morpheme_cls)
                for candidate_str, candidate in candidates.items()
            },
        )


@dataclass(frozen=True)
class PageCandidateTermList:
    page_num: int
    candidates: List[Term]

    def to_json(self) -> Dict[str, Any]:
        return {
            "page_num": self.page_num,
            "candidates": list(map(lambda term: term.to_json(), self.candidates)),
        }

    @classmethod
    def from_json(
        cls,
        obj: Dict[str, Any],
        morpheme_cls: Type[BaseMeCabMorpheme] = MeCabMorphemeIPADic,
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

    def to_json(self) -> Dict[str, Any]:
        return {
            "pdf_path": self.pdf_path,
            "pages": list(map(lambda page: page.to_json(), self.pages)),
        }

    @classmethod
    def from_json(
        cls,
        obj: Dict[str, Any],
        morpheme_cls: Type[BaseMeCabMorpheme] = MeCabMorphemeIPADic,
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

    def to_domain_candidate_term_dict(self) -> DomainCandidateTermDict:
        candidates: Dict[str, Term] = dict()
        for pdf in self.pdfs:
            for page in pdf.pages:
                for candidate in page.candidates:
                    candidate_str = str(candidate)
                    candidate_in_dict = candidates.get(
                        candidate_str, Term(candidate.morphemes, 0.0, True)
                    )
                    candidates[candidate_str] = Term(
                        candidate.morphemes,
                        max(candidate.fontsize, candidate_in_dict.fontsize),
                        candidate.augmented and candidate_in_dict.augmented,
                    )

        return DomainCandidateTermDict(self.domain, candidates)

    def to_domain_candidate_term_set(self) -> DomainCandidateTermSet:
        return DomainCandidateTermSet(
            self.domain,
            {
                str(candidate)
                for pdf in self.pdfs
                for page in pdf.pages
                for candidate in page.candidates
            },
        )

    def to_json(self) -> Dict[str, Any]:
        return {
            "domain": self.domain,
            "pdfs": list(map(lambda pdf: pdf.to_json(), self.pdfs)),
        }

    @classmethod
    def from_json(
        cls,
        obj: Dict[str, Any],
        morpheme_cls: Type[BaseMeCabMorpheme] = MeCabMorphemeIPADic,
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
