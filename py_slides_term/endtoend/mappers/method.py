from typing import Dict, Any, Union, Type

from py_slides_term.methods.single import (
    BaseSingleDomainRankingMethod,
    MCValueMethod,
    FLRMethod,
    HITSMethod,
    FLRHMethod,
)
from py_slides_term.methods.multi import (
    BaseMultiDomainRankingMethod,
    TFIDFMethod,
    LFIDFMethod,
    MDPMethod,
)


class RankingMethodMapper:
    def __init__(self):
        self._single_domain_clses: Dict[
            str, Type[BaseSingleDomainRankingMethod[Any]]
        ] = dict()
        self._multi_domain_clses: Dict[
            str, Type[BaseMultiDomainRankingMethod[Any]]
        ] = dict()

    def add_single_domain_method_cls(
        self, name: str, method_cls: Type[BaseSingleDomainRankingMethod[Any]]
    ):
        if name is None:
            name = f"{method_cls.__module__}.{method_cls.__name__}"

        self._single_domain_clses[name] = method_cls

    def add_multi_domain_method_cls(
        self, name: str, method_cls: Type[BaseMultiDomainRankingMethod[Any]]
    ):
        if name is None:
            name = f"{method_cls.__module__}.{method_cls.__name__}"

        self._multi_domain_clses[name] = method_cls

    def find_single_domain_method_cls(
        self, name: str
    ) -> Union[Type[BaseSingleDomainRankingMethod[Any]], None]:
        return self._single_domain_clses.get(name)

    def find_multi_domain_method_cls(
        self, name: str
    ) -> Union[Type[BaseMultiDomainRankingMethod[Any]], None]:
        return self._multi_domain_clses.get(name)

    @classmethod
    def default_mapper(cls):
        default = cls()

        default.add_single_domain_method_cls(
            "py_slides_term.methods.single.MCValueMethod", MCValueMethod
        )
        default.add_single_domain_method_cls(
            "py_slides_term.methods.single.FLRMethod", FLRMethod
        )
        default.add_single_domain_method_cls(
            "py_slides_term.methods..single.HITSMethod", HITSMethod
        )
        default.add_single_domain_method_cls(
            "py_slides_term.methods.single.FLRHMethod", FLRHMethod
        )

        default.add_multi_domain_method_cls(
            "py_slides_term.methods.multi.TFIDFMethod", TFIDFMethod
        )
        default.add_multi_domain_method_cls(
            "py_slides_term.methods.multi.LFIDFMethod", LFIDFMethod
        )
        default.add_multi_domain_method_cls(
            "py_slides_term.methods.multi.MDPMethod", MDPMethod
        )

        return default
