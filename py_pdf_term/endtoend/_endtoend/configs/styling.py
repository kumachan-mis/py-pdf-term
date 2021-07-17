from dataclasses import dataclass, field
from typing import List

from .base import BaseLayerConfig


@dataclass(frozen=True)
class StylingLayerConfig(BaseLayerConfig):
    styling_scores: List[str] = field(
        default_factory=lambda: [
            "py_pdf_term.FontsizeScore",
            "py_pdf_term.ColorScore",
        ]
    )
    cache: str = "py_pdf_term.StylingLayerFileCache"
