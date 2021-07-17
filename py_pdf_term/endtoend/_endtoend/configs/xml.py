from dataclasses import dataclass
from typing import Optional

from .base import BaseLayerConfig
from py_pdf_term._common.consts import JAPANESE_REGEX, ENGLISH_REGEX, NUMBER_REGEX


@dataclass(frozen=True)
class XMLLayerConfig(BaseLayerConfig):
    open_bin: str = "python.open"
    include_pattern: Optional[str] = rf"{ENGLISH_REGEX}|{JAPANESE_REGEX}|{NUMBER_REGEX}"
    exclude_pattern: Optional[str] = None
    nfc_norm: bool = True
    cache: str = "py_pdf_term.XMLLayerFileCache"
