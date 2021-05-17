from dataclasses import dataclass, field
from typing import List

from .base import BaseLayerConfig


@dataclass(frozen=True)
class StylingLayerConfig(BaseLayerConfig):
    styling_scores: List[str] = field(
        default_factory=lambda: [
            "py_slides_term.FontsizeScore",
            "py_slides_term.ColorScore",
        ]
    )
    cache: str = "py_slides_term.StylingLayerFileCache"
    remove_lower_layer_cache: bool = False
