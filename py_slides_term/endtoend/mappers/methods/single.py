from typing import Type, Any

from ..base import BaseMapper
from py_slides_term.methods import (
    BaseSingleDomainRankingMethod,
    MCValueMethod,
    FLRMethod,
    HITSMethod,
    FLRHMethod,
)


class SingleDomainRankingMethodMapper(
    BaseMapper[Type[BaseSingleDomainRankingMethod[Any]]]
):
    @classmethod
    def default_mapper(cls):
        module_path = "py_slides_term.methods"
        default_mapper = cls()

        single_domain_clses = [MCValueMethod, FLRMethod, HITSMethod, FLRHMethod]
        for method_cls in single_domain_clses:
            default_mapper.add(f"{module_path}.{method_cls.__name__}", method_cls)

        return default_mapper
