from typing import Any, Self

from py_pdf_term._common.consts import PACKAGE_NAME
from py_pdf_term.methods import (
    BaseSingleDomainRankingMethod,
    FLRHMethod,
    FLRMethod,
    HITSMethod,
    MCValueMethod,
)

from ..base import BaseMapper


class SingleDomainRankingMethodMapper(
    BaseMapper[type[BaseSingleDomainRankingMethod[Any]]]
):
    """Mapper to find single-domain ranking method classes."""

    @classmethod
    def default_mapper(cls) -> Self:
        default_mapper = cls()

        single_domain_clses: list[type[BaseSingleDomainRankingMethod[Any]]] = [
            MCValueMethod,
            FLRMethod,
            HITSMethod,
            FLRHMethod,
        ]
        for method_cls in single_domain_clses:
            default_mapper.add(f"{PACKAGE_NAME}.{method_cls.__name__}", method_cls)

        return default_mapper
