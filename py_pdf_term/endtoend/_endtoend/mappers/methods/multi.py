from typing import Any, Self

from py_pdf_term._common.consts import PACKAGE_NAME
from py_pdf_term.methods import BaseMultiDomainRankingMethod, MDPMethod, TFIDFMethod

from ..base import BaseMapper


class MultiDomainRankingMethodMapper(
    BaseMapper[type[BaseMultiDomainRankingMethod[Any]]]
):
    """Mapper to find multi-domain ranking method classes."""

    @classmethod
    def default_mapper(cls) -> Self:
        default_mapper = cls()

        multi_domain_clses: list[type[BaseMultiDomainRankingMethod[Any]]] = [
            TFIDFMethod,
            MDPMethod,
        ]
        for method_cls in multi_domain_clses:
            default_mapper.add(f"{PACKAGE_NAME}.{method_cls.__name__}", method_cls)

        return default_mapper
