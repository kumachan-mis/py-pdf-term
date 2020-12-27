from dataclasses import dataclass
from typing import List, Dict, Callable

from pdf_slides_term.share.data import TechnicalTerm
from pdf_slides_term.mecab.morphemes import BaseMeCabMorpheme, MeCabMorphemeIPADic


@dataclass
class PageCandidateTermList:
    page_num: int
    candidates: List[TechnicalTerm]

    def to_json(self) -> Dict:
        return {
            "page_num": self.page_num,
            "candidates": list(map(lambda term: term.to_json(), self.candidates)),
        }

    @classmethod
    def from_json(
        cls,
        obj: Dict,
        morpheme_cls: Callable[[str], BaseMeCabMorpheme] = MeCabMorphemeIPADic,
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


@dataclass
class XMLCandidateTermList:
    xml_path: str
    pages: List[PageCandidateTermList]

    def to_json(self) -> Dict:
        return {
            "xml_path": self.xml_path,
            "pages": list(map(lambda page: page.to_json(), self.pages)),
        }

    @classmethod
    def from_json(
        cls,
        obj: Dict,
        morpheme_cls: Callable[[str], BaseMeCabMorpheme] = MeCabMorphemeIPADic,
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


@dataclass
class DomainCandidateTermList:
    domain: str
    xmls: List[XMLCandidateTermList]

    def to_json(self) -> Dict:
        return {
            "domain": self.domain,
            "xmls": list(map(lambda xml: xml.to_json(), self.xmls)),
        }

    @classmethod
    def from_json(
        cls,
        obj: Dict,
        morpheme_cls: Callable[[str], BaseMeCabMorpheme] = MeCabMorphemeIPADic,
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
