from dataclasses import dataclass
from typing import Optional

from .base import BaseLayerConfig


@dataclass(frozen=True)
class XMLLayerConfig(BaseLayerConfig):
    open_bin: str = "python.open"
    include_pattern: Optional[str] = None
    exclude_pattern: Optional[str] = None
    nfc_norm: bool = True
    cache: str = "py_pdf_term.XMLLayerFileCache"
