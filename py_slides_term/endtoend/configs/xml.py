from dataclasses import dataclass

from .base import BaseLayerConfig


@dataclass(frozen=True)
class XMLLayerConfig(BaseLayerConfig):
    use_cache: bool = True
