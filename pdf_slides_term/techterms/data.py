from dataclasses import dataclass, asdict
from typing import List, Dict, Any


@dataclass(frozen=True)
class PageTechnicalTermList:
    page_num: int
    terms: List[str]

    def to_json(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_json(cls, obj: Dict[str, Any]):
        return cls(**obj)


@dataclass
class XMLTechnicalTermList:
    xml_path: str
    pages: List[PageTechnicalTermList]

    def to_json(self) -> Dict[str, Any]:
        return {
            "xml_path": self.xml_path,
            "pages": list(map(lambda page: page.to_json(), self.pages)),
        }

    @classmethod
    def from_json(cls, obj: Dict[str, Any]):
        xml_path, pages = obj["xml_path"], obj["pages"]
        return cls(
            xml_path,
            list(map(lambda item: PageTechnicalTermList.from_json(item), pages)),
        )


@dataclass(frozen=True)
class DomainTechnicalTermList:
    domain: str
    xmls: List[XMLTechnicalTermList]

    def to_json(self) -> Dict[str, Any]:
        return {
            "domain": self.domain,
            "xmls": list(map(lambda xml: xml.to_json(), self.xmls)),
        }

    @classmethod
    def from_json(cls, obj: Dict[str, Any]):
        domain, xmls = obj["domain"], obj["xmls"]
        return cls(
            domain,
            list(map(lambda item: XMLTechnicalTermList.from_json(item), xmls)),
        )


@dataclass(frozen=True)
class DomainTermScoreDict:
    domain: str
    term_scores: Dict[str, float]
