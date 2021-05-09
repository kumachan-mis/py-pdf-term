from dataclasses import dataclass

from .base import BaseLayerConfig


@dataclass(frozen=True)
class XMLLayerConfig(BaseLayerConfig):
    apply_nfc_normalization: bool = True
    cache: str = "py_slides_term.caches.XMLLayerFileCache"
