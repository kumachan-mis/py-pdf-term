from dataclasses import dataclass

from .base import BaseLayerConfig


@dataclass(frozen=True)
class AnalysisLayerConfig(BaseLayerConfig):
    use_cache: bool = True
