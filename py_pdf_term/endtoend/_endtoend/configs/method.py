from dataclasses import dataclass, field
from typing import Any, Dict

from .base import BaseLayerConfig


@dataclass(frozen=True)
class MethodLayerConfig(BaseLayerConfig):
    method_type: str = "single"
    method: str = "py_pdf_term.FLRHMethod"
    hyper_params: Dict[str, Any] = field(default_factory=dict)
    ranking_cache: str = "py_pdf_term.MethodLayerRankingFileCache"
    data_cache: str = "py_pdf_term.MethodLayerRankingFileCache"
