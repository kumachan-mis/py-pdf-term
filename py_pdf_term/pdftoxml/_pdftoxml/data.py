from dataclasses import asdict, dataclass
from typing import Any, Dict
from xml.etree.ElementTree import Element, fromstring, tostring


@dataclass(frozen=True)
class PDFnXMLPath:
    """Pair of path to a PDF file and that to a XML file.

    Args
    ----
        pdf_path:
            Path to a PDF file.
        xml_path:
            Path to a XML file.
    """

    pdf_path: str
    xml_path: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> "PDFnXMLPath":
        return cls(**obj)


@dataclass(frozen=True)
class PDFnXMLElement:
    """Pair of path to a PDF file and XML element tree.

    Args
    ----
        pdf_path:
            Path to a PDF file.
        xml_root:
            Root element of a XML element tree.
    """

    pdf_path: str
    xml_root: Element

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pdf_path": self.pdf_path,
            "xml_root": tostring(self.xml_root, encoding="utf-8").decode("utf-8"),
        }

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> "PDFnXMLElement":
        return cls(obj["pdf_path"], fromstring(obj["xml_root"]))
