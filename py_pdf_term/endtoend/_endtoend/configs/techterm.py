from dataclasses import dataclass

from .base import BaseLayerConfig


@dataclass(frozen=True)
class TechnicalTermLayerConfig(BaseLayerConfig):
    max_num_terms: int = 10
    acceptance_rate: float = 0.75
