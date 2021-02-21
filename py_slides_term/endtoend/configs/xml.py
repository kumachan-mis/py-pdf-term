from dataclasses import dataclass

from .base import BaseLayerConfig


@dataclass(frozen=True)
class XMLLayerConfig(BaseLayerConfig):
    apply_nfc_normalization: bool = True
    use_cache: bool = True
