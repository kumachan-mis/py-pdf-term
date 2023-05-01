from typing import Any, Type

from py_pdf_term._common.consts import PACKAGE_NAME
from py_pdf_term.methods import BaseMultiDomainRankingMethod, MDPMethod, TFIDFMethod

from ..base import BaseMapper


class MultiDomainRankingMethodMapper(
    BaseMapper[Type[BaseMultiDomainRankingMethod[Any]]]
):
    """A mapper to find multi-domain ranking method classes."""

    @classmethod
    def default_mapper(cls) -> "MultiDomainRankingMethodMapper":
        default_mapper = cls()

        multi_domain_clses = [TFIDFMethod, MDPMethod]
        for method_cls in multi_domain_clses:
            default_mapper.add(f"{PACKAGE_NAME}.{method_cls.__name__}", method_cls)

        return default_mapper
