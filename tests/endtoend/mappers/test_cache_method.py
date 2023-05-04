from pytest import raises
from typing import Any

from py_pdf_term.mappers import (
    MethodLayerDataCacheMapper,
    MethodLayerRankingCacheMapper,
)
from py_pdf_term.endtoend.caches import (
    MethodLayerDataNoCache,
    MethodLayerDataFileCache,
    MethodLayerRankingNoCache,
    MethodLayerRankingFileCache,
)


def test_data_default_mapper_find():
    mapper = MethodLayerDataCacheMapper.default_mapper()

    cls = mapper.find("py_pdf_term.MethodLayerDataNoCache")
    assert cls == MethodLayerDataNoCache[Any]
    cls = mapper.find("py_pdf_term.MethodLayerDataFileCache")
    assert cls == MethodLayerDataFileCache[Any]

    raises(KeyError, lambda: mapper.find("py_pdf_term.MethodLayerDataUnknownCache"))


def test_data_default_mapper_find_or_none():
    mapper = MethodLayerDataCacheMapper.default_mapper()

    cls = mapper.find_or_none("py_pdf_term.MethodLayerDataNoCache")
    assert cls == MethodLayerDataNoCache[Any]
    cls = mapper.find_or_none("py_pdf_term.MethodLayerDataFileCache")
    assert cls == MethodLayerDataFileCache[Any]
    cls = mapper.find_or_none("py_pdf_term.MethodLayerDataUnknownCache")
    assert cls is None


def test_data_default_mapper_bulk_find():
    mapper = MethodLayerDataCacheMapper.default_mapper()

    clses = mapper.bulk_find(
        ["py_pdf_term.MethodLayerDataNoCache", "py_pdf_term.MethodLayerDataFileCache"]
    )
    assert clses == [MethodLayerDataNoCache[Any], MethodLayerDataFileCache[Any]]

    raises(
        KeyError, lambda: mapper.bulk_find(["py_pdf_term.MethodLayerDataUnknownCache"])
    )


def test_data_default_mapper_bulk_find_or_none():
    mapper = MethodLayerDataCacheMapper.default_mapper()

    clses = mapper.bulk_find_or_none(
        [
            "py_pdf_term.MethodLayerDataNoCache",
            "py_pdf_term.MethodLayerDataFileCache",
            "py_pdf_term.MethodLayerDataUnknownCache",
        ]
    )
    assert clses == [MethodLayerDataNoCache[Any], MethodLayerDataFileCache[Any], None]


def test_data_mapper_add_then_remove():
    mapper = MethodLayerDataCacheMapper()

    mapper.add("py_pdf_term.MethodLayerDataNoCache", MethodLayerDataNoCache[Any])

    cls = mapper.find("py_pdf_term.MethodLayerDataNoCache")
    assert cls == MethodLayerDataNoCache[Any]

    mapper.remove("py_pdf_term.MethodLayerDataNoCache")

    raises(KeyError, lambda: mapper.find("py_pdf_term.MethodLayerDataNoCache"))


def test_ranking_default_mapper_find():
    mapper = MethodLayerRankingCacheMapper.default_mapper()

    cls = mapper.find("py_pdf_term.MethodLayerRankingNoCache")
    assert cls == MethodLayerRankingNoCache
    cls = mapper.find("py_pdf_term.MethodLayerRankingFileCache")
    assert cls == MethodLayerRankingFileCache

    raises(KeyError, lambda: mapper.find("py_pdf_term.MethodLayerRankingUnknownCache"))


def test_ranking_default_mapper_find_or_none():
    mapper = MethodLayerRankingCacheMapper.default_mapper()

    cls = mapper.find_or_none("py_pdf_term.MethodLayerRankingNoCache")
    assert cls == MethodLayerRankingNoCache
    cls = mapper.find_or_none("py_pdf_term.MethodLayerRankingFileCache")
    assert cls == MethodLayerRankingFileCache
    cls = mapper.find_or_none("py_pdf_term.MethodLayerRankingUnknownCache")
    assert cls is None


def test_ranking_default_mapper_bulk_find():
    mapper = MethodLayerRankingCacheMapper.default_mapper()

    clses = mapper.bulk_find(
        [
            "py_pdf_term.MethodLayerRankingNoCache",
            "py_pdf_term.MethodLayerRankingFileCache",
        ]
    )
    assert clses == [MethodLayerRankingNoCache, MethodLayerRankingFileCache]

    raises(
        KeyError,
        lambda: mapper.bulk_find(["py_pdf_term.MethodLayerRankingUnknownCache"]),
    )


def test_ranking_default_mapper_bulk_find_or_none():
    mapper = MethodLayerRankingCacheMapper.default_mapper()

    clses = mapper.bulk_find_or_none(
        [
            "py_pdf_term.MethodLayerRankingNoCache",
            "py_pdf_term.MethodLayerRankingFileCache",
            "py_pdf_term.MethodLayerRankingUnknownCache",
        ]
    )
    assert clses == [MethodLayerRankingNoCache, MethodLayerRankingFileCache, None]


def test_ranking_mapper_add_then_remove():
    mapper = MethodLayerRankingCacheMapper()

    mapper.add("py_pdf_term.MethodLayerRankingNoCache", MethodLayerRankingNoCache)

    cls = mapper.find("py_pdf_term.MethodLayerRankingNoCache")
    assert cls == MethodLayerRankingNoCache

    mapper.remove("py_pdf_term.MethodLayerRankingNoCache")

    raises(KeyError, lambda: mapper.find("py_pdf_term.MethodLayerRankingNoCache"))
