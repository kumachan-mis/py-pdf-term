from dataclasses import dataclass

from .base import BaseLayerConfig


@dataclass(frozen=True)
class XMLLayerConfig(BaseLayerConfig):
    """Configuration for an XML layer.

    Args
    ----
        bin_opener:
            Binary opener class name. The default opener is
            "py_pdf_term.StandardBinaryOpener".
        include_pattern:
            Regular expression pattern of text to include in the output.
        exclude_pattern:
            Regular expression pattern of text to exclude from the output (overrides
            include_pattern).
        nfc_norm:
            If True, normalize text to NFC, otherwise keep original.
        cache:
            Cache class name. The default cache is "py_pdf_term.XMLLayerFileCache".
    """

    bin_opener: str = "py_pdf_term.StandardBinaryOpener"
    include_pattern: str | None = None
    exclude_pattern: str | None = None
    nfc_norm: bool = True
    cache: str = "py_pdf_term.XMLLayerFileCache"
