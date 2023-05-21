import json
from pathlib import Path
from typing import Any, Type

from pytest import mark, raises
from pytest_mock import MockerFixture

from py_pdf_term import DomainPDFList
from py_pdf_term.candidates import DomainCandidateTermList, PDFCandidateTermList
from py_pdf_term.configs import (
    MultiDomainMethodLayerConfig,
    SingleDomainMethodLayerConfig,
)
from py_pdf_term.endtoend._endtoend.layers import (
    CandidateLayer,
    MultiDomainMethodLayer,
    SingleDomainMethodLayer,
)
from py_pdf_term.endtoend.caches import (
    MethodLayerDataNoCache,
    MethodLayerRankingNoCache,
)
from py_pdf_term.mappers import (
    MethodLayerDataCacheMapper,
    MethodLayerRankingCacheMapper,
    MultiDomainRankingMethodMapper,
    SingleDomainRankingMethodMapper,
)
from py_pdf_term.methods import (
    BaseMultiDomainRankingMethod,
    BaseSingleDomainRankingMethod,
    FLRHMethod,
    FLRMethod,
    HITSMethod,
    MCValueMethod,
    MDPMethod,
    TFIDFMethod,
)

from ...fixtures import PyPDFTermFixture, WikipediaPDFFixture


class TestCandidateLayer(CandidateLayer):
    __test__ = False

    def __init__(self) -> None:
        pass

    def create_candidates(self, domain_pdfs: DomainPDFList) -> DomainCandidateTermList:
        if domain_pdfs.domain == "test":
            return DomainCandidateTermList(
                "test", [self.create_pdf_candidates(PyPDFTermFixture.PDF_PATH)]
            )
        elif domain_pdfs.domain == "other":
            return DomainCandidateTermList(
                "other", [self.create_pdf_candidates(WikipediaPDFFixture.PDF_PATH)]
            )
        else:
            raise ValueError(f"Unknown domain: {domain_pdfs.domain}")

    def create_pdf_candidates(self, pdf_path: str) -> PDFCandidateTermList:
        if pdf_path == PyPDFTermFixture.PDF_PATH:
            candidate_path = PyPDFTermFixture.CANDIDATE_PATH
        elif pdf_path == WikipediaPDFFixture.PDF_PATH:
            candidate_path = WikipediaPDFFixture.CANDIDATE_PATH
        else:
            raise ValueError(f"Unknown PDF path: {pdf_path}")

        with open(candidate_path, "r") as f:
            obj = json.load(f)
            obj["pdf_path"] = pdf_path
        return PDFCandidateTermList.from_dict(obj)

    def remove_cache(self, pdf_path: str) -> None:
        pass


class TestSingleDomainMethod(MCValueMethod):
    __test__ = False


class TestMultiDomainMethod(MDPMethod):
    __test__ = False


class TestMethodLayerDataCache(MethodLayerDataNoCache[Any]):
    __test__ = False


class TestMethodLayerRankingCache(MethodLayerRankingNoCache):
    __test__ = False


def test_single_minimal_config(tmp_path: Path) -> None:
    method_layer = SingleDomainMethodLayer(
        candidate_layer=TestCandidateLayer(),
        cache_dir=tmp_path.as_posix(),
    )

    ranking = method_layer.create_term_ranking(
        DomainPDFList("test", [PyPDFTermFixture.PDF_PATH])
    )

    PyPDFTermFixture.assert_method_term_ranking(ranking)


def test_multi_minimal_config(tmp_path: Path) -> None:
    method_layer = MultiDomainMethodLayer(
        candidate_layer=TestCandidateLayer(),
        cache_dir=tmp_path.as_posix(),
    )

    ranking = method_layer.create_term_ranking(
        "test",
        [
            DomainPDFList("test", [PyPDFTermFixture.PDF_PATH]),
            DomainPDFList("other", [WikipediaPDFFixture.PDF_PATH]),
        ],
    )

    PyPDFTermFixture.assert_method_term_ranking(ranking, acceptance_rate=0.85)


def test_single_full_config(tmp_path: Path) -> None:
    method_mapper = SingleDomainRankingMethodMapper()
    method_mapper.add("test.TestSingleDomainMethod", TestSingleDomainMethod)
    ranking_cache_mapper = MethodLayerRankingCacheMapper()
    ranking_cache_mapper.add(
        "test.TestMethodLayerRankingCache", TestMethodLayerRankingCache
    )
    data_cache_mapper = MethodLayerDataCacheMapper()
    data_cache_mapper.add("test.TestMethodLayerDataCache", TestMethodLayerDataCache)

    config = SingleDomainMethodLayerConfig(
        method="test.TestSingleDomainMethod",
        hyper_params={},
        ranking_cache="test.TestMethodLayerRankingCache",
        data_cache="test.TestMethodLayerDataCache",
    )
    method_layer = SingleDomainMethodLayer(
        candidate_layer=TestCandidateLayer(),
        config=config,
        method_mapper=method_mapper,
        data_cache_mapper=data_cache_mapper,
        ranking_cache_mapper=ranking_cache_mapper,
        cache_dir=tmp_path.as_posix(),
    )

    ranking = method_layer.create_term_ranking(
        DomainPDFList("test", [PyPDFTermFixture.PDF_PATH])
    )

    PyPDFTermFixture.assert_method_term_ranking(ranking)


def test_multi_full_config(tmp_path: Path) -> None:
    method_mapper = MultiDomainRankingMethodMapper()
    method_mapper.add("test.TestMultiDomainMethod", TestMultiDomainMethod)
    ranking_cache_mapper = MethodLayerRankingCacheMapper()
    ranking_cache_mapper.add(
        "test.TestMethodLayerRankingCache", TestMethodLayerRankingCache
    )
    data_cache_mapper = MethodLayerDataCacheMapper()
    data_cache_mapper.add("test.TestMethodLayerDataCache", TestMethodLayerDataCache)

    config = MultiDomainMethodLayerConfig(
        method="test.TestMultiDomainMethod",
        hyper_params={},
        ranking_cache="test.TestMethodLayerRankingCache",
        data_cache="test.TestMethodLayerDataCache",
    )
    method_layer = MultiDomainMethodLayer(
        candidate_layer=TestCandidateLayer(),
        config=config,
        method_mapper=method_mapper,
        data_cache_mapper=data_cache_mapper,
        ranking_cache_mapper=ranking_cache_mapper,
        cache_dir=tmp_path.as_posix(),
    )

    ranking = method_layer.create_term_ranking(
        "test",
        [
            DomainPDFList("test", [PyPDFTermFixture.PDF_PATH]),
            DomainPDFList("other", [WikipediaPDFFixture.PDF_PATH]),
        ],
    )

    PyPDFTermFixture.assert_method_term_ranking(ranking, acceptance_rate=0.85)


@mark.parametrize(
    "method, method_class",
    [
        ("py_pdf_term.MCValueMethod", MCValueMethod),
        ("py_pdf_term.FLRMethod", FLRMethod),
        ("py_pdf_term.HITSMethod", HITSMethod),
        ("py_pdf_term.FLRHMethod", FLRHMethod),
    ],
)
def test_single_data_file_cache(
    tmp_path: Path,
    mocker: MockerFixture,
    method: str,
    method_class: Type[BaseSingleDomainRankingMethod[Any]],
) -> None:
    spied_collect_data = mocker.spy(method_class, "collect_data")
    spied_rank_terms = mocker.spy(method_class, "rank_terms")

    method_layer = SingleDomainMethodLayer(
        candidate_layer=TestCandidateLayer(),
        config=SingleDomainMethodLayerConfig(
            method=method,
            ranking_cache="py_pdf_term.MethodLayerRankingNoCache",
        ),
        cache_dir=tmp_path.as_posix(),
    )

    ranking = method_layer.create_term_ranking(
        DomainPDFList("test", [PyPDFTermFixture.PDF_PATH])
    )

    assert spied_collect_data.call_count == 1
    assert spied_rank_terms.call_count == 1
    PyPDFTermFixture.assert_method_term_ranking(ranking)

    ranking = method_layer.create_term_ranking(
        DomainPDFList("test", [PyPDFTermFixture.PDF_PATH])
    )

    assert spied_collect_data.call_count == 1
    assert spied_rank_terms.call_count == 2
    PyPDFTermFixture.assert_method_term_ranking(ranking)

    method_layer.remove_cache([PyPDFTermFixture.PDF_PATH])
    ranking = method_layer.create_term_ranking(
        DomainPDFList("test", [PyPDFTermFixture.PDF_PATH])
    )

    assert spied_collect_data.call_count == 2
    assert spied_rank_terms.call_count == 3
    PyPDFTermFixture.assert_method_term_ranking(ranking)


@mark.parametrize(
    "method, method_class",
    [
        ("py_pdf_term.TFIDFMethod", TFIDFMethod),
        ("py_pdf_term.MDPMethod", MDPMethod),
    ],
)
def test_multi_data_file_cache(
    tmp_path: Path,
    mocker: MockerFixture,
    method: str,
    method_class: Type[BaseMultiDomainRankingMethod[Any]],
) -> None:
    spied_collect_data = mocker.spy(method_class, "collect_data")
    spied_rank_domain_terms = mocker.spy(method_class, "rank_domain_terms")

    method_layer = MultiDomainMethodLayer(
        candidate_layer=TestCandidateLayer(),
        config=MultiDomainMethodLayerConfig(
            method=method,
            ranking_cache="py_pdf_term.MethodLayerRankingNoCache",
        ),
        cache_dir=tmp_path.as_posix(),
    )

    ranking = method_layer.create_term_ranking(
        "test",
        [
            DomainPDFList("test", [PyPDFTermFixture.PDF_PATH]),
            DomainPDFList("other", [WikipediaPDFFixture.PDF_PATH]),
        ],
    )

    assert spied_collect_data.call_count == 2
    assert spied_rank_domain_terms.call_count == 1
    PyPDFTermFixture.assert_method_term_ranking(ranking, acceptance_rate=0.85)

    ranking = method_layer.create_term_ranking(
        "test",
        [
            DomainPDFList("test", [PyPDFTermFixture.PDF_PATH]),
            DomainPDFList("other", [WikipediaPDFFixture.PDF_PATH]),
        ],
    )

    assert spied_collect_data.call_count == 2
    assert spied_rank_domain_terms.call_count == 2
    PyPDFTermFixture.assert_method_term_ranking(ranking, acceptance_rate=0.85)

    method_layer.remove_cache([PyPDFTermFixture.PDF_PATH])
    method_layer.remove_cache([WikipediaPDFFixture.PDF_PATH])
    ranking = method_layer.create_term_ranking(
        "test",
        [
            DomainPDFList("test", [PyPDFTermFixture.PDF_PATH]),
            DomainPDFList("other", [WikipediaPDFFixture.PDF_PATH]),
        ],
    )

    assert spied_collect_data.call_count == 4
    assert spied_rank_domain_terms.call_count == 3
    PyPDFTermFixture.assert_method_term_ranking(ranking, acceptance_rate=0.85)


@mark.parametrize(
    "method, method_class",
    [
        ("py_pdf_term.MCValueMethod", MCValueMethod),
        ("py_pdf_term.FLRMethod", FLRMethod),
        ("py_pdf_term.HITSMethod", HITSMethod),
        ("py_pdf_term.FLRHMethod", FLRHMethod),
    ],
)
def test_single_ranking_file_cache(
    tmp_path: Path,
    mocker: MockerFixture,
    method: str,
    method_class: Type[BaseSingleDomainRankingMethod[Any]],
) -> None:
    spied_collect_data = mocker.spy(method_class, "collect_data")
    spied_rank_terms = mocker.spy(method_class, "rank_terms")

    method_layer = SingleDomainMethodLayer(
        candidate_layer=TestCandidateLayer(),
        config=SingleDomainMethodLayerConfig(
            method=method,
            data_cache="py_pdf_term.MethodLayerDataNoCache",
        ),
        cache_dir=tmp_path.as_posix(),
    )

    ranking = method_layer.create_term_ranking(
        DomainPDFList("test", [PyPDFTermFixture.PDF_PATH])
    )

    assert spied_collect_data.call_count == 1
    assert spied_rank_terms.call_count == 1
    PyPDFTermFixture.assert_method_term_ranking(ranking)

    ranking = method_layer.create_term_ranking(
        DomainPDFList("test", [PyPDFTermFixture.PDF_PATH])
    )

    assert spied_collect_data.call_count == 1
    assert spied_rank_terms.call_count == 1
    PyPDFTermFixture.assert_method_term_ranking(ranking)

    method_layer.remove_cache([PyPDFTermFixture.PDF_PATH])
    ranking = method_layer.create_term_ranking(
        DomainPDFList("test", [PyPDFTermFixture.PDF_PATH])
    )

    assert spied_collect_data.call_count == 2
    assert spied_rank_terms.call_count == 2
    PyPDFTermFixture.assert_method_term_ranking(ranking)


@mark.parametrize(
    "method, method_class",
    [
        ("py_pdf_term.TFIDFMethod", TFIDFMethod),
        ("py_pdf_term.MDPMethod", MDPMethod),
    ],
)
def test_multi_ranking_file_cache(
    tmp_path: Path,
    mocker: MockerFixture,
    method: str,
    method_class: Type[BaseMultiDomainRankingMethod[Any]],
) -> None:
    spied_collect_data = mocker.spy(method_class, "collect_data")
    spied_rank_domain_terms = mocker.spy(method_class, "rank_domain_terms")

    method_layer = MultiDomainMethodLayer(
        candidate_layer=TestCandidateLayer(),
        config=MultiDomainMethodLayerConfig(
            method=method,
            data_cache="py_pdf_term.MethodLayerDataNoCache",
        ),
        cache_dir=tmp_path.as_posix(),
    )

    ranking = method_layer.create_term_ranking(
        "test",
        [
            DomainPDFList("test", [PyPDFTermFixture.PDF_PATH]),
            DomainPDFList("other", [WikipediaPDFFixture.PDF_PATH]),
        ],
    )

    assert spied_collect_data.call_count == 2
    assert spied_rank_domain_terms.call_count == 1
    PyPDFTermFixture.assert_method_term_ranking(ranking, acceptance_rate=0.85)

    ranking = method_layer.create_term_ranking(
        "test",
        [
            DomainPDFList("test", [PyPDFTermFixture.PDF_PATH]),
            DomainPDFList("other", [WikipediaPDFFixture.PDF_PATH]),
        ],
    )

    assert spied_collect_data.call_count == 2
    assert spied_rank_domain_terms.call_count == 1
    PyPDFTermFixture.assert_method_term_ranking(ranking, acceptance_rate=0.85)

    method_layer.remove_cache([PyPDFTermFixture.PDF_PATH])
    method_layer.remove_cache([WikipediaPDFFixture.PDF_PATH])
    ranking = method_layer.create_term_ranking(
        "test",
        [
            DomainPDFList("test", [PyPDFTermFixture.PDF_PATH]),
            DomainPDFList("other", [WikipediaPDFFixture.PDF_PATH]),
        ],
    )

    assert spied_collect_data.call_count == 4
    assert spied_rank_domain_terms.call_count == 2
    PyPDFTermFixture.assert_method_term_ranking(ranking, acceptance_rate=0.85)


@mark.parametrize(
    "method, method_class",
    [
        ("py_pdf_term.MCValueMethod", MCValueMethod),
        ("py_pdf_term.FLRMethod", FLRMethod),
        ("py_pdf_term.HITSMethod", HITSMethod),
        ("py_pdf_term.FLRHMethod", FLRHMethod),
    ],
)
def test_single_no_cache(
    tmp_path: Path,
    mocker: MockerFixture,
    method: str,
    method_class: Type[BaseSingleDomainRankingMethod[Any]],
) -> None:
    spied_collect_data = mocker.spy(method_class, "collect_data")
    spied_rank_terms = mocker.spy(method_class, "rank_terms")

    method_layer = SingleDomainMethodLayer(
        candidate_layer=TestCandidateLayer(),
        config=SingleDomainMethodLayerConfig(
            method=method,
            ranking_cache="py_pdf_term.MethodLayerRankingNoCache",
            data_cache="py_pdf_term.MethodLayerDataNoCache",
        ),
        cache_dir=tmp_path.as_posix(),
    )

    ranking = method_layer.create_term_ranking(
        DomainPDFList("test", [PyPDFTermFixture.PDF_PATH])
    )

    assert spied_collect_data.call_count == 1
    assert spied_rank_terms.call_count == 1
    PyPDFTermFixture.assert_method_term_ranking(ranking)

    ranking = method_layer.create_term_ranking(
        DomainPDFList("test", [PyPDFTermFixture.PDF_PATH])
    )

    assert spied_collect_data.call_count == 2
    assert spied_rank_terms.call_count == 2
    PyPDFTermFixture.assert_method_term_ranking(ranking)

    method_layer.remove_cache([PyPDFTermFixture.PDF_PATH])
    ranking = method_layer.create_term_ranking(
        DomainPDFList("test", [PyPDFTermFixture.PDF_PATH])
    )

    assert spied_collect_data.call_count == 3
    assert spied_rank_terms.call_count == 3
    PyPDFTermFixture.assert_method_term_ranking(ranking)


@mark.parametrize(
    "method, method_class",
    [
        ("py_pdf_term.TFIDFMethod", TFIDFMethod),
        ("py_pdf_term.MDPMethod", MDPMethod),
    ],
)
def test_multi_no_cache(
    tmp_path: Path,
    mocker: MockerFixture,
    method: str,
    method_class: Type[BaseMultiDomainRankingMethod[Any]],
) -> None:
    spied_collect_data = mocker.spy(method_class, "collect_data")
    spied_rank_domain_terms = mocker.spy(method_class, "rank_domain_terms")

    method_layer = MultiDomainMethodLayer(
        candidate_layer=TestCandidateLayer(),
        config=MultiDomainMethodLayerConfig(
            method=method,
            ranking_cache="py_pdf_term.MethodLayerRankingNoCache",
            data_cache="py_pdf_term.MethodLayerDataNoCache",
        ),
        cache_dir=tmp_path.as_posix(),
    )

    ranking = method_layer.create_term_ranking(
        "test",
        [
            DomainPDFList("test", [PyPDFTermFixture.PDF_PATH]),
            DomainPDFList("other", [WikipediaPDFFixture.PDF_PATH]),
        ],
    )

    assert spied_collect_data.call_count == 2
    assert spied_rank_domain_terms.call_count == 1
    PyPDFTermFixture.assert_method_term_ranking(ranking, acceptance_rate=0.85)

    ranking = method_layer.create_term_ranking(
        "test",
        [
            DomainPDFList("test", [PyPDFTermFixture.PDF_PATH]),
            DomainPDFList("other", [WikipediaPDFFixture.PDF_PATH]),
        ],
    )

    assert spied_collect_data.call_count == 4
    assert spied_rank_domain_terms.call_count == 2
    PyPDFTermFixture.assert_method_term_ranking(ranking, acceptance_rate=0.85)

    method_layer.remove_cache([PyPDFTermFixture.PDF_PATH])
    method_layer.remove_cache([WikipediaPDFFixture.PDF_PATH])
    ranking = method_layer.create_term_ranking(
        "test",
        [
            DomainPDFList("test", [PyPDFTermFixture.PDF_PATH]),
            DomainPDFList("other", [WikipediaPDFFixture.PDF_PATH]),
        ],
    )

    assert spied_collect_data.call_count == 6
    assert spied_rank_domain_terms.call_count == 3
    PyPDFTermFixture.assert_method_term_ranking(ranking, acceptance_rate=0.85)


@mark.parametrize(
    "invalid_config, expected_exception",
    [
        (
            SingleDomainMethodLayerConfig(method="py_pdf_term.UnknownMethod"),
            KeyError,
        ),
        (
            SingleDomainMethodLayerConfig(hyper_params={"unknown": 0}),
            TypeError,
        ),
        (
            SingleDomainMethodLayerConfig(
                ranking_cache="py_pdf_term.UnknownMethodRankingCache"
            ),
            KeyError,
        ),
        (
            SingleDomainMethodLayerConfig(
                data_cache="py_pdf_term.UnknownMethodDataCache"
            ),
            KeyError,
        ),
        (
            SingleDomainMethodLayerConfig(
                method="py_pdf_term.HITSMethod",
                hyper_params={"threshold": "invalid"},
            ),
            TypeError,
        ),
        (
            SingleDomainMethodLayerConfig(
                method="py_pdf_term.HITSMethod",
                hyper_params={"max_loop": "invalid"},
            ),
            TypeError,
        ),
        (
            SingleDomainMethodLayerConfig(
                method="py_pdf_term.HITSMethod",
                hyper_params={"threshold": -1e-8},
            ),
            ValueError,
        ),
        (
            SingleDomainMethodLayerConfig(
                method="py_pdf_term.HITSMethod",
                hyper_params={"max_loop": 0},
            ),
            ValueError,
        ),
        (
            SingleDomainMethodLayerConfig(
                method="py_pdf_term.FLRHMethod",
                hyper_params={"threshold": "invalid"},
            ),
            TypeError,
        ),
        (
            SingleDomainMethodLayerConfig(
                method="py_pdf_term.FLRHMethod",
                hyper_params={"max_loop": "invalid"},
            ),
            TypeError,
        ),
        (
            SingleDomainMethodLayerConfig(
                method="py_pdf_term.FLRHMethod",
                hyper_params={"threshold": 0.0},
            ),
            ValueError,
        ),
        (
            SingleDomainMethodLayerConfig(
                method="py_pdf_term.FLRHMethod",
                hyper_params={"max_loop": 0},
            ),
            ValueError,
        ),
    ],
)
def test_single_invalid_config(
    tmp_path: Path,
    invalid_config: SingleDomainMethodLayerConfig,
    expected_exception: Type[Exception],
) -> None:
    raises(
        expected_exception,
        lambda: SingleDomainMethodLayer(
            candidate_layer=TestCandidateLayer(),
            config=invalid_config,
            cache_dir=tmp_path.as_posix(),
        ),
    )


@mark.parametrize(
    "invalid_config, expected_exception",
    [
        (
            MultiDomainMethodLayerConfig(method="py_pdf_term.UnknownMethod"),
            KeyError,
        ),
        (
            MultiDomainMethodLayerConfig(hyper_params={"unknown": 0}),
            TypeError,
        ),
        (
            MultiDomainMethodLayerConfig(
                ranking_cache="py_pdf_term.UnknownMethodRankingCache"
            ),
            KeyError,
        ),
        (
            MultiDomainMethodLayerConfig(
                data_cache="py_pdf_term.UnknownMethodDataCache"
            ),
            KeyError,
        ),
        (
            MultiDomainMethodLayerConfig(
                method="py_pdf_term.TFIDFMethod",
                hyper_params={"tfmode": 0},
            ),
            TypeError,
        ),
        (
            MultiDomainMethodLayerConfig(
                method="py_pdf_term.TFIDFMethod",
                hyper_params={"idfmode": 0},
            ),
            TypeError,
        ),
        (
            MultiDomainMethodLayerConfig(
                method="py_pdf_term.TFIDFMethod",
                hyper_params={"tfmode": "invalid"},
            ),
            TypeError,
        ),
        (
            MultiDomainMethodLayerConfig(
                method="py_pdf_term.TFIDFMethod",
                hyper_params={"idfmode": "invalid"},
            ),
            TypeError,
        ),
    ],
)
def test_multi_invalid_config(
    tmp_path: Path,
    invalid_config: MultiDomainMethodLayerConfig,
    expected_exception: Type[Exception],
) -> None:
    raises(
        expected_exception,
        lambda: MultiDomainMethodLayer(
            candidate_layer=TestCandidateLayer(),
            config=invalid_config,
            cache_dir=tmp_path.as_posix(),
        ),
    )
