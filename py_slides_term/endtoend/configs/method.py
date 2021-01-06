from dataclasses import dataclass, field
from typing import Dict, Any, Literal

from .base import BaseLayerConfig


@dataclass(frozen=True)
class MethodLayerConfig(BaseLayerConfig):
    method_type: Literal["single", "multi"] = "single"
    method: str = "py_slides_term.methods.MCValueMethod"
    hyper_params: Dict[str, Any] = field(default_factory=dict)
    use_cache: bool = True
    remove_lower_layer_cache_when_completed: bool = True
