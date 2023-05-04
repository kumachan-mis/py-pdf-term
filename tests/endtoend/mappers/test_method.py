from py_pdf_term.mappers import (
    MultiDomainRankingMethodMapper,
    SingleDomainRankingMethodMapper,
)
from py_pdf_term.methods import (
    FLRHMethod,
    FLRMethod,
    HITSMethod,
    MCValueMethod,
    MDPMethod,
    TFIDFMethod,
)


def test_single_domain_ranking_method_default_mapper() -> None:
    mapper = SingleDomainRankingMethodMapper.default_mapper()

    clses = mapper.bulk_find_or_none(
        [
            "py_pdf_term.MCValueMethod",
            "py_pdf_term.FLRMethod",
            "py_pdf_term.HITSMethod",
            "py_pdf_term.FLRHMethod",
            "py_pdf_term.UnknownMethod",
        ]
    )
    assert clses == [MCValueMethod, FLRMethod, HITSMethod, FLRHMethod, None]


def test_multi_domain_ranking_method_default_mapper() -> None:
    mapper = MultiDomainRankingMethodMapper.default_mapper()

    clses = mapper.bulk_find_or_none(
        [
            "py_pdf_term.TFIDFMethod",
            "py_pdf_term.MDPMethod",
            "py_pdf_term.UnknownMethod",
        ]
    )
    assert clses == [TFIDFMethod, MDPMethod, None]
