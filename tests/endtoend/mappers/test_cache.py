from typing import Any

from py_pdf_term.mappers import (
    CandidateLayerCacheMapper,
    XMLLayerCacheMapper,
    MethodLayerDataCacheMapper,
    MethodLayerRankingCacheMapper,
    StylingLayerCacheMapper,
)
from py_pdf_term.endtoend.caches import (
    CandidateLayerNoCache,
    CandidateLayerFileCache,
    XMLLayerNoCache,
    XMLLayerFileCache,
    MethodLayerDataNoCache,
    MethodLayerDataFileCache,
    MethodLayerRankingNoCache,
    MethodLayerRankingFileCache,
    StylingLayerNoCache,
    StylingLayerFileCache,
)


def test_xml_layer_cache_default_mapper() -> None:
    mapper = XMLLayerCacheMapper.default_mapper()

    clses = mapper.bulk_find_or_none(
        [
            "py_pdf_term.XMLLayerNoCache",
            "py_pdf_term.XMLLayerFileCache",
            "py_pdf_term.XMLLayerUnknownCache",
        ]
    )
    assert clses == [XMLLayerNoCache, XMLLayerFileCache, None]


def test_candidate_layer_cache_default_mapper() -> None:
    mapper = CandidateLayerCacheMapper.default_mapper()

    clses = mapper.bulk_find_or_none(
        [
            "py_pdf_term.CandidateLayerNoCache",
            "py_pdf_term.CandidateLayerFileCache",
            "py_pdf_term.CandidateLayerUnknownCache",
        ]
    )
    assert clses == [CandidateLayerNoCache, CandidateLayerFileCache, None]


def test_method_layer_data_cache_default_mapper() -> None:
    mapper = MethodLayerDataCacheMapper.default_mapper()

    clses = mapper.bulk_find_or_none(
        [
            "py_pdf_term.MethodLayerDataNoCache",
            "py_pdf_term.MethodLayerDataFileCache",
            "py_pdf_term.MethodLayerDataUnknownCache",
        ]
    )
    assert clses == [MethodLayerDataNoCache[Any], MethodLayerDataFileCache[Any], None]


def test_method_layer_ranking_cache_default_mapper() -> None:
    mapper = MethodLayerRankingCacheMapper.default_mapper()

    clses = mapper.bulk_find_or_none(
        [
            "py_pdf_term.MethodLayerRankingNoCache",
            "py_pdf_term.MethodLayerRankingFileCache",
            "py_pdf_term.MethodLayerRankingUnknownCache",
        ]
    )
    assert clses == [MethodLayerRankingNoCache, MethodLayerRankingFileCache, None]


def test_styling_layer_cache_default_mapper() -> None:
    mapper = StylingLayerCacheMapper.default_mapper()

    clses = mapper.bulk_find_or_none(
        [
            "py_pdf_term.StylingLayerNoCache",
            "py_pdf_term.StylingLayerFileCache",
            "py_pdf_term.StylingLayerUnknownCache",
        ]
    )
    assert clses == [StylingLayerNoCache, StylingLayerFileCache, None]
