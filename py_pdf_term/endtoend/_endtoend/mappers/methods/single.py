from typing import Any, Type

from py_pdf_term.methods import (
    BaseSingleDomainRankingMethod,
    FLRHMethod,
    FLRMethod,
    HITSMethod,
    MCValueMethod,
)

from ..base import BaseMapper
from ..consts import PACKAGE_NAME


class SingleDomainRankingMethodMapper(
    BaseMapper[Type[BaseSingleDomainRankingMethod[Any]]]
):
    @classmethod
    def default_mapper(cls) -> "SingleDomainRankingMethodMapper":
        default_mapper = cls()

        single_domain_clses = [MCValueMethod, FLRMethod, HITSMethod, FLRHMethod]
        for method_cls in single_domain_clses:
            default_mapper.add(f"{PACKAGE_NAME}.{method_cls.__name__}", method_cls)

        return default_mapper
