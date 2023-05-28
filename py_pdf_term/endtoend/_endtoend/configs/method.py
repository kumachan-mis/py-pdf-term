from dataclasses import dataclass, field
from typing import Any

from .base import BaseLayerConfig


@dataclass(frozen=True)
class BaseMethodLayerConfig(BaseLayerConfig):
    method: str
    hyper_params: dict[str, Any] = field(default_factory=dict)
    ranking_cache: str = "py_pdf_term.MethodLayerRankingFileCache"
    data_cache: str = "py_pdf_term.MethodLayerDataFileCache"


@dataclass(frozen=True)
class SingleDomainMethodLayerConfig(BaseMethodLayerConfig):
    """Configuration for a single-domain method layer.

    Args:
        method:
            Single-domain method class name. The default method is
            "py_pdf_term.FLRHMethod".
        hyper_params:
            Hyper parameters for the method. The default hyper parameters are
            empty.
        ranking_cache:
            Ranking cache class name. The default cache is
            "py_pdf_term.MethodLayerRankingFileCache".
        data_cache:
            Data cache class name. The default cache is
            "py_pdf_term.MethodLayerDataFileCache".
    """

    method: str = "py_pdf_term.FLRHMethod"


@dataclass(frozen=True)
class MultiDomainMethodLayerConfig(BaseMethodLayerConfig):
    """Configuration for a multi-domain method layer.

    Args
    ----
        method:
            Multi-domain method class name. The default method is
            "py_pdf_term.TFIDFMethod".
        hyper_params:
            Hyper parameters for the method. The default hyper parameters are
            empty.
        ranking_cache:
            Ranking cache class name. The default cache is
            "py_pdf_term.MethodLayerRankingFileCache".
        data_cache:
            Data cache class name. The default cache is
            "py_pdf_term.MethodLayerDataFileCache".
    """

    method: str = "py_pdf_term.TFIDFMethod"
