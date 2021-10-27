from typing import Any, Type

from py_pdf_term.methods import (
    BaseMultiDomainRankingMethod,
    LFIDFMethod,
    MDPMethod,
    TFIDFMethod,
)

from ..base import BaseMapper
from ..consts import PACKAGE_NAME


class MultiDomainRankingMethodMapper(
    BaseMapper[Type[BaseMultiDomainRankingMethod[Any]]]
):
    @classmethod
    def default_mapper(cls) -> "MultiDomainRankingMethodMapper":
        default_mapper = cls()

        multi_domain_clses = [TFIDFMethod, LFIDFMethod, MDPMethod]
        for method_cls in multi_domain_clses:
            default_mapper.add(f"{PACKAGE_NAME}.{method_cls.__name__}", method_cls)

        return default_mapper
