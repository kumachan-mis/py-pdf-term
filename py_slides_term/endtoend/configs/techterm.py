from dataclasses import dataclass

from .base import BaseLayerConfig


@dataclass(frozen=True)
class TechnicalTermLayerConfig(BaseLayerConfig):
    max_num_pageterms: int = 14
    acceptance_rate: float = 0.9
