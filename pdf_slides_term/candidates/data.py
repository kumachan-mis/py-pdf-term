from dataclasses import dataclass
from typing import List, Dict, Any, Type

from pdf_slides_term.share.data import TechnicalTerm
from pdf_slides_term.mecab.morphemes import BaseMeCabMorpheme, MeCabMorphemeIPADic


@dataclass(frozen=True)
class DomainCandidateTermDict:
    domain: str
    candidates: Dict[str, TechnicalTerm]

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
        return cls(
            obj["domain"],
            {
                candidate_str: TechnicalTerm.from_json(candidate, morpheme_cls)
                for candidate_str, candidate in obj["candidates"].items()
            },
        )


@dataclass(frozen=True)
class PageCandidateTermList:
    page_num: int
    candidates: List[TechnicalTerm]

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
        return cls(
            obj["page_num"],
            list(
                map(
                    lambda item: TechnicalTerm.from_json(item, morpheme_cls),
                    obj["candidates"],
                )
            ),
        )


@dataclass(frozen=True)
class XMLCandidateTermList:
    xml_path: str
    pages: List[PageCandidateTermList]

    def to_json(self) -> Dict[str, Any]:
        return {
            "xml_path": self.xml_path,
            "pages": list(map(lambda page: page.to_json(), self.pages)),
        }

    @classmethod
    def from_json(
        cls,
        obj: Dict[str, Any],
        morpheme_cls: Type[BaseMeCabMorpheme] = MeCabMorphemeIPADic,
    ):
        return cls(
            obj["xml_path"],
            list(
                map(
                    lambda item: PageCandidateTermList.from_json(item, morpheme_cls),
                    obj["pages"],
                )
            ),
        )


@dataclass(frozen=True)
class DomainCandidateTermList:
    domain: str
    xmls: List[XMLCandidateTermList]

    def to_domain_candidate_term_dict(self) -> DomainCandidateTermDict:
        return DomainCandidateTermDict(
            self.domain,
            {
                str(candidate): candidate
                for xml in self.xmls
                for page in xml.pages
                for candidate in page.candidates
            },
        )

    def to_json(self) -> Dict[str, Any]:
        return {
            "domain": self.domain,
            "xmls": list(map(lambda xml: xml.to_json(), self.xmls)),
        }

    @classmethod
    def from_json(
        cls,
        obj: Dict[str, Any],
        morpheme_cls: Type[BaseMeCabMorpheme] = MeCabMorphemeIPADic,
    ):
        return cls(
            obj["domain"],
            list(
                map(
                    lambda item: XMLCandidateTermList.from_json(item, morpheme_cls),
                    obj["xmls"],
                )
            ),
        )
