from dataclasses import dataclass, asdict
from typing import Dict, Any


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
