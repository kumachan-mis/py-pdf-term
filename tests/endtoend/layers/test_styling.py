import json
from pathlib import Path

from pytest import mark, raises
from pytest_mock import MockerFixture

from py_pdf_term import DomainPDFList
from py_pdf_term.candidates import DomainCandidateTermList, PDFCandidateTermList
from py_pdf_term.configs import StylingLayerConfig
from py_pdf_term.endtoend._endtoend.layers import CandidateLayer, StylingLayer
from py_pdf_term.endtoend.caches import StylingLayerNoCache
from py_pdf_term.mappers import StylingLayerCacheMapper, StylingScoreMapper
from py_pdf_term.stylings import StylingScorer
from py_pdf_term.stylings.scores import FontsizeScore

from ...fixtures import PyPDFTermFixture


class TestCandidateLayer(CandidateLayer):
    __test__ = False

    def __init__(self) -> None:
        pass

    def create_candidates(self, domain_pdfs: DomainPDFList) -> DomainCandidateTermList:
        return DomainCandidateTermList(
            "test", [self.create_pdf_candidates(PyPDFTermFixture.PDF_PATH)]
        )

    def create_pdf_candidates(self, pdf_path: str) -> PDFCandidateTermList:
        with open(PyPDFTermFixture.CANDIDATE_PATH, "r") as f:
            obj = json.load(f)
            obj["pdf_path"] = pdf_path
        return PDFCandidateTermList.from_dict(obj)

    def remove_cache(self, pdf_path: str) -> None:
        pass


class TestStylingScore(FontsizeScore):
    __test__ = False


class TestStylingLayerCache(StylingLayerNoCache):
    __test__ = False


def test_mimimal_config(tmp_path: Path) -> None:
    styling_layer = StylingLayer(
        candidate_layer=TestCandidateLayer(), cache_dir=tmp_path.as_posix()
    )

    pdf_stylings = styling_layer.create_pdf_styling_scores(PyPDFTermFixture.PDF_PATH)

    PyPDFTermFixture.assert_pdf_stylings(pdf_stylings)


def test_full_config(tmp_path: Path) -> None:
    config = StylingLayerConfig(
        styling_scores=["test.TestStylingScore"],
        cache="test.TestStylingLayerCache",
    )
    styling_score_mapper = StylingScoreMapper()
    styling_score_mapper.add("test.TestStylingScore", TestStylingScore)
    cache_mapper = StylingLayerCacheMapper()
    cache_mapper.add("test.TestStylingLayerCache", TestStylingLayerCache)

    styling_layer = StylingLayer(
        candidate_layer=TestCandidateLayer(),
        config=config,
        styling_score_mapper=styling_score_mapper,
        cache_mapper=cache_mapper,
        cache_dir=tmp_path.as_posix(),
    )

    pdf_stylings = styling_layer.create_pdf_styling_scores(PyPDFTermFixture.PDF_PATH)

    PyPDFTermFixture.assert_pdf_stylings(pdf_stylings)


def test_file_cache(tmp_path: Path, mocker: MockerFixture) -> None:
    spied_score_pdf_candidates = mocker.spy(StylingScorer, "score_pdf_candidates")

    styling_layer = StylingLayer(
        candidate_layer=TestCandidateLayer(), cache_dir=tmp_path.as_posix()
    )

    pdf_stylings = styling_layer.create_pdf_styling_scores(PyPDFTermFixture.PDF_PATH)

    assert spied_score_pdf_candidates.call_count == 1
    PyPDFTermFixture.assert_pdf_stylings(pdf_stylings)

    pdf_stylings = styling_layer.create_pdf_styling_scores(PyPDFTermFixture.PDF_PATH)

    assert spied_score_pdf_candidates.call_count == 1
    PyPDFTermFixture.assert_pdf_stylings(pdf_stylings)

    styling_layer.remove_cache(PyPDFTermFixture.PDF_PATH)
    pdf_stylings = styling_layer.create_pdf_styling_scores(PyPDFTermFixture.PDF_PATH)

    assert spied_score_pdf_candidates.call_count == 2
    PyPDFTermFixture.assert_pdf_stylings(pdf_stylings)


def test_no_cache(tmp_path: Path, mocker: MockerFixture) -> None:
    spied_score_pdf_candidates = mocker.spy(StylingScorer, "score_pdf_candidates")

    styling_layer = StylingLayer(
        candidate_layer=TestCandidateLayer(),
        config=StylingLayerConfig(cache="py_pdf_term.StylingLayerNoCache"),
        cache_dir=tmp_path.as_posix(),
    )

    pdf_stylings = styling_layer.create_pdf_styling_scores(PyPDFTermFixture.PDF_PATH)

    assert spied_score_pdf_candidates.call_count == 1
    PyPDFTermFixture.assert_pdf_stylings(pdf_stylings)

    pdf_stylings = styling_layer.create_pdf_styling_scores(PyPDFTermFixture.PDF_PATH)

    assert spied_score_pdf_candidates.call_count == 2
    PyPDFTermFixture.assert_pdf_stylings(pdf_stylings)

    styling_layer.remove_cache(PyPDFTermFixture.PDF_PATH)
    pdf_stylings = styling_layer.create_pdf_styling_scores(PyPDFTermFixture.PDF_PATH)

    assert spied_score_pdf_candidates.call_count == 3
    PyPDFTermFixture.assert_pdf_stylings(pdf_stylings)


@mark.parametrize(
    "invalid_config, expected_exception",
    [
        (
            StylingLayerConfig(styling_scores=["py_pdf_term.UnknownScore"]),
            KeyError,
        ),
        (
            StylingLayerConfig(cache="py_pdf_term.UnknownStylingLayerCache"),
            KeyError,
        ),
    ],
)
def test_invalid_config(
    tmp_path: Path,
    invalid_config: StylingLayerConfig,
    expected_exception: type[Exception],
) -> None:
    raises(
        expected_exception,
        lambda: StylingLayer(
            candidate_layer=TestCandidateLayer(),
            config=invalid_config,
            cache_dir=tmp_path.as_posix(),
        ),
    )
