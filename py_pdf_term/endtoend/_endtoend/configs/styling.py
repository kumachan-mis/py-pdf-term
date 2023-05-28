from dataclasses import dataclass, field

from .base import BaseLayerConfig


@dataclass(frozen=True)
class StylingLayerConfig(BaseLayerConfig):
    """Configuration for a styling layer.

    Args
    ----
        styling_scores:
            List of styling score class names. The default scores are
            "py_pdf_term.FontsizeScore" and "py_pdf_term.ColorScore".
        cache:
            Cache class name. The default cache is
            "py_pdf_term.StylingLayerFileCache".
    """

    styling_scores: list[str] = field(
        default_factory=lambda: [
            "py_pdf_term.FontsizeScore",
            "py_pdf_term.ColorScore",
        ]
    )
    cache: str = "py_pdf_term.StylingLayerFileCache"
