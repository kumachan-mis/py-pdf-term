from dataclasses import dataclass

from .base import BaseLayerConfig


@dataclass(frozen=True)
class StylingLayerConfig(BaseLayerConfig):
    cache: str = "py_slides_term.StylingLayerFileCache"
    remove_lower_layer_cache: bool = False
