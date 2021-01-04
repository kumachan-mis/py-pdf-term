from typing import Dict, Any, Union, Type

from py_slides_term.methods import (
    BaseSingleDomainRankingMethod,
    BaseMultiDomainRankingMethod,
    MCValueMethod,
    TFIDFMethod,
    LFIDFMethod,
    FLRMethod,
    HITSMethod,
    FLRHMethod,
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
            "py_slides_term.methods.MCValueMethod", MCValueMethod
        )
        default.add_single_domain_method_cls(
            "py_slides_term.methods.FLRMethod", FLRMethod
        )
        default.add_single_domain_method_cls(
            "py_slides_term.methods.HITSMethod", HITSMethod
        )
        default.add_single_domain_method_cls(
            "py_slides_term.methods.FLRHMethod", FLRHMethod
        )

        default.add_multi_domain_method_cls(
            "py_slides_term.methods.TFIDFMethod", TFIDFMethod
        )
        default.add_multi_domain_method_cls(
            "py_slides_term.methods.LFIDFMethod", LFIDFMethod
        )
        default.add_multi_domain_method_cls(
            "py_slides_term.methods.MDPMethod", MDPMethod
        )

        return default
