from dataclasses import dataclass, field
from typing import Dict, Any, Literal

from .base import BaseLayerConfig


@dataclass(frozen=True)
class MethodLayerConfig(BaseLayerConfig):
    method_type: Literal["single", "multi"] = "single"
    method: str = "py_slides_term.FLRHMethod"
    hyper_params: Dict[str, Any] = field(default_factory=dict)
    ranking_cache: str = "py_slides_term.MethodLayerRankingFileCache"
    data_cache: str = "py_slides_term.MethodLayerRankingFileCache"
    remove_lower_layer_cache: bool = False
