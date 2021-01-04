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
        module_path = "py_slides_term.methods"
        default_mapper = cls()

        single_domain_clses = [MCValueMethod, FLRMethod, HITSMethod, FLRHMethod]
        for method_cls in single_domain_clses:
            default_mapper.add_single_domain_method_cls(
                f"{module_path}.{method_cls.__name__}", method_cls
            )

        multi_domain_clses = [TFIDFMethod, LFIDFMethod, MDPMethod]
        for method_cls in multi_domain_clses:
            default_mapper.add_multi_domain_method_cls(
                f"{module_path}.{method_cls.__name__}", method_cls
            )

        return default_mapper
