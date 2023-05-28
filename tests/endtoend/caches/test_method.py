from dataclasses import dataclass
from pathlib import Path
from typing import Any

from py_pdf_term._common.data import ScoredTerm
from py_pdf_term.configs import (
    MultiDomainMethodLayerConfig,
    SingleDomainMethodLayerConfig,
)
from py_pdf_term.endtoend.caches import (
    MethodLayerDataFileCache,
    MethodLayerDataNoCache,
    MethodLayerRankingFileCache,
    MethodLayerRankingNoCache,
)
from py_pdf_term.methods import MethodTermRanking
from py_pdf_term.methods.rankingdata import BaseRankingData


@dataclass(frozen=True)
class TestRankingData(BaseRankingData):
    __test__ = False

    freq_dict: dict[str, int]

    @classmethod
    def from_dict(cls, obj: dict[str, Any]) -> "TestRankingData":
        return TestRankingData(**obj)


def test_data_file_cache(tmp_path: Path) -> None:
    cache = MethodLayerDataFileCache[TestRankingData](tmp_path.as_posix())

    pdf_paths = ["test1.pdf", "test2.pdf"]
    first_ranking_data = TestRankingData("test", {"term": 1})
    second_ranking_data = TestRankingData("test", {"term": 2})
    config = SingleDomainMethodLayerConfig(method="test.TestMethod")

    assert cache.load(pdf_paths, config, TestRankingData.from_dict) is None

    cache.store(pdf_paths, first_ranking_data, config)
    assert (
        cache.load(pdf_paths, config, TestRankingData.from_dict) == first_ranking_data
    )

    cache.store(pdf_paths, second_ranking_data, config)
    assert (
        cache.load(pdf_paths, config, TestRankingData.from_dict) == second_ranking_data
    )

    cache.remove(pdf_paths, config)
    assert cache.load(pdf_paths, config, TestRankingData.from_dict) is None

    cache.remove(pdf_paths, config)
    assert cache.load(pdf_paths, config, TestRankingData.from_dict) is None


def test_data_file_cache_multiple(tmp_path: Path) -> None:
    cache = MethodLayerDataFileCache[TestRankingData](tmp_path.as_posix())

    pdf_paths1 = ["test1-1.pdf", "test1-2.pdf"]
    ranking_data1 = TestRankingData("test1", {"term": 1})
    pdf_paths2 = ["test2-1.pdf", "test2-2.pdf"]
    ranking_data2 = TestRankingData("test2", {"term": 2})
    config = SingleDomainMethodLayerConfig(method="test.TestMethod")

    assert cache.load(pdf_paths1, config, TestRankingData.from_dict) is None
    assert cache.load(pdf_paths2, config, TestRankingData.from_dict) is None

    cache.store(pdf_paths1, ranking_data1, config)
    assert cache.load(pdf_paths1, config, TestRankingData.from_dict) == ranking_data1
    assert cache.load(pdf_paths2, config, TestRankingData.from_dict) is None

    cache.store(pdf_paths2, ranking_data2, config)
    assert cache.load(pdf_paths1, config, TestRankingData.from_dict) == ranking_data1
    assert cache.load(pdf_paths2, config, TestRankingData.from_dict) == ranking_data2

    cache.remove(pdf_paths1, config)
    assert cache.load(pdf_paths1, config, TestRankingData.from_dict) is None
    assert cache.load(pdf_paths2, config, TestRankingData.from_dict) == ranking_data2

    cache.remove(pdf_paths2, config)
    assert cache.load(pdf_paths1, config, TestRankingData.from_dict) is None
    assert cache.load(pdf_paths2, config, TestRankingData.from_dict) is None


def test_data_no_cache(tmp_path: Path) -> None:
    cache = MethodLayerDataNoCache[TestRankingData](tmp_path.as_posix())

    pdf_paths = ["test1.pdf", "test2.pdf"]
    first_ranking_data = TestRankingData("test", {"term": 1})
    second_ranking_data = TestRankingData("test", {"term": 2})
    config = SingleDomainMethodLayerConfig(method="test.TestMethod")

    assert cache.load(pdf_paths, config, TestRankingData.from_dict) is None

    cache.store(pdf_paths, first_ranking_data, config)
    assert cache.load(pdf_paths, config, TestRankingData.from_dict) is None

    cache.store(pdf_paths, second_ranking_data, config)
    assert cache.load(pdf_paths, config, TestRankingData.from_dict) is None

    cache.remove(pdf_paths, config)
    assert cache.load(pdf_paths, config, TestRankingData.from_dict) is None

    cache.remove(pdf_paths, config)
    assert cache.load(pdf_paths, config, TestRankingData.from_dict) is None


def test_ranking_file_cache(tmp_path: Path) -> None:
    cache = MethodLayerRankingFileCache(tmp_path.as_posix())

    pdf_paths = ["test1.pdf", "test2.pdf"]
    first_ranking = MethodTermRanking(
        "test",
        [
            ScoredTerm("rare term", 2.0),
            ScoredTerm("technical term", 1.0),
            ScoredTerm("common word", 0.5),
        ],
    )
    second_ranking = MethodTermRanking(
        "test2",
        [
            ScoredTerm("rare term", 5.0),
            ScoredTerm("technical term", 2.5),
            ScoredTerm("common word", 0.0),
        ],
    )
    config = MultiDomainMethodLayerConfig(method="test.TestMethod")

    assert cache.load(pdf_paths, config) is None

    cache.store(pdf_paths, first_ranking, config)
    assert cache.load(pdf_paths, config) == first_ranking

    cache.store(pdf_paths, second_ranking, config)
    assert cache.load(pdf_paths, config) == second_ranking

    cache.remove(pdf_paths, config)
    assert cache.load(pdf_paths, config) is None

    cache.remove(pdf_paths, config)
    assert cache.load(pdf_paths, config) is None


def test_ranking_file_cache_multiple(tmp_path: Path) -> None:
    cache = MethodLayerRankingFileCache(tmp_path.as_posix())

    pdf_paths1 = ["test1-1.pdf", "test1-2.pdf"]
    ranking1 = MethodTermRanking(
        "test1",
        [
            ScoredTerm("rare term", 2.0),
            ScoredTerm("technical term", 1.0),
            ScoredTerm("common word", 0.5),
        ],
    )
    pdf_paths2 = ["test2-1.pdf", "test2-2.pdf"]
    ranking2 = MethodTermRanking(
        "test2",
        [
            ScoredTerm("rare term", 5.0),
            ScoredTerm("technical term", 2.5),
            ScoredTerm("common word", 0.0),
        ],
    )
    config = MultiDomainMethodLayerConfig(method="test.TestMethod")

    assert cache.load(pdf_paths1, config) is None
    assert cache.load(pdf_paths2, config) is None

    cache.store(pdf_paths1, ranking1, config)
    assert cache.load(pdf_paths1, config) == ranking1
    assert cache.load(pdf_paths2, config) is None

    cache.store(pdf_paths2, ranking2, config)
    assert cache.load(pdf_paths1, config) == ranking1
    assert cache.load(pdf_paths2, config) == ranking2

    cache.remove(pdf_paths1, config)
    assert cache.load(pdf_paths1, config) is None
    assert cache.load(pdf_paths2, config) == ranking2

    cache.remove(pdf_paths2, config)
    assert cache.load(pdf_paths1, config) is None
    assert cache.load(pdf_paths2, config) is None


def test_ranking_no_cache(tmp_path: Path) -> None:
    cache = MethodLayerRankingNoCache(tmp_path.as_posix())

    pdf_paths = ["test1.pdf", "test2.pdf"]
    first_ranking = MethodTermRanking(
        "test",
        [
            ScoredTerm("rare term", 2.0),
            ScoredTerm("technical term", 1.0),
            ScoredTerm("common word", 0.5),
        ],
    )
    second_ranking = MethodTermRanking(
        "test2",
        [
            ScoredTerm("rare term", 5.0),
            ScoredTerm("technical term", 2.5),
            ScoredTerm("common word", 0.0),
        ],
    )
    config = MultiDomainMethodLayerConfig(method="test.TestMethod")

    assert cache.load(pdf_paths, config) is None

    cache.store(pdf_paths, first_ranking, config)
    assert cache.load(pdf_paths, config) is None

    cache.store(pdf_paths, second_ranking, config)
    assert cache.load(pdf_paths, config) is None

    cache.remove(pdf_paths, config)
    assert cache.load(pdf_paths, config) is None

    cache.remove(pdf_paths, config)
    assert cache.load(pdf_paths, config) is None
