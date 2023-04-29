from dataclasses import dataclass, field
from typing import Any, Dict

from .base import BaseLayerConfig


@dataclass(frozen=True)
class BaseMethodLayerConfig(BaseLayerConfig):
    method: str
    hyper_params: Dict[str, Any] = field(default_factory=dict)
    ranking_cache: str = "py_pdf_term.MethodLayerRankingFileCache"
    data_cache: str = "py_pdf_term.MethodLayerRankingFileCache"


@dataclass(frozen=True)
class SingleDomainMethodLayerConfig(BaseMethodLayerConfig):
    method: str = "py_pdf_term.FLRHMethod"


@dataclass(frozen=True)
class MultiDomainMethodLayerConfig(BaseMethodLayerConfig):
    method: str = "py_pdf_term.TFIDFMethod"
