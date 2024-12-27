from dataclasses import asdict, dataclass
from typing import Any, Self
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

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, obj: dict[str, Any]) -> Self:
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

    def __eq__(self, other: Any) -> bool:
        return (
            isinstance(other, PDFnXMLElement)
            and self.pdf_path == other.pdf_path
            and tostring(self.xml_root) == tostring(other.xml_root)
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "pdf_path": self.pdf_path,
            "xml_root": tostring(self.xml_root, encoding="utf-8"),
        }

    @classmethod
    def from_dict(cls, obj: dict[str, Any]) -> Self:
        return cls(obj["pdf_path"], fromstring(obj["xml_root"]))
