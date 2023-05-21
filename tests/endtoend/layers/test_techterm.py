import json
from typing import List, Type

from pytest import mark, raises

from py_pdf_term import DomainPDFList
from py_pdf_term.candidates import DomainCandidateTermList, PDFCandidateTermList
from py_pdf_term.configs import TechnicalTermLayerConfig
from py_pdf_term.endtoend._endtoend.layers import (
    CandidateLayer,
    MultiDomainMethodLayer,
    MultiDomainTechnicalTermLayer,
    SingleDomainMethodLayer,
    SingleDomainTechnicalTermLayer,
    StylingLayer,
)
from py_pdf_term.methods import MethodTermRanking
from py_pdf_term.stylings import PDFStylingScoreList

from ...fixtures import PyPDFTermFixture, WikipediaPDFFixture


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


class TestStylingLayer(StylingLayer):
    __test__ = False

    def __init__(self) -> None:
        pass

    def create_pdf_styling_scores(self, pdf_path: str) -> PDFStylingScoreList:
        with open(PyPDFTermFixture.STYLING_PATH, "r") as f:
            obj = json.load(f)
            obj["pdf_path"] = pdf_path
        return PDFStylingScoreList.from_dict(obj)

    def remove_cache(self, pdf_path: str) -> None:
        pass


class TestSingleDomainMethodLayer(SingleDomainMethodLayer):
    __test__ = False

    def __init__(self) -> None:
        pass

    def create_term_ranking(self, domain_pdfs: DomainPDFList) -> MethodTermRanking:
        with open(PyPDFTermFixture.METHOD_PATH, "r") as f:
            obj = json.load(f)
        return MethodTermRanking.from_dict(obj)


class TestMultiDomainMethodLayer(MultiDomainMethodLayer):
    __test__ = False

    def __init__(self) -> None:
        pass

    def create_term_ranking(
        self, domain: str, multi_domain_pdfs: List[DomainPDFList]
    ) -> MethodTermRanking:
        with open(PyPDFTermFixture.METHOD_PATH, "r") as f:
            obj = json.load(f)
        return MethodTermRanking.from_dict(obj)


def test_single_minimal_config() -> None:
    techterm_layer = SingleDomainTechnicalTermLayer(
        candidate_layer=TestCandidateLayer(),
        styling_layer=TestStylingLayer(),
        method_layer=TestSingleDomainMethodLayer(),
    )

    pdf_techterms = techterm_layer.create_pdf_techterms(
        PyPDFTermFixture.PDF_PATH, DomainPDFList("test", [PyPDFTermFixture.PDF_PATH])
    )

    PyPDFTermFixture.assert_pdf_techterms(pdf_techterms)


def test_multi_minimal_config() -> None:
    techterm_layer = MultiDomainTechnicalTermLayer(
        candidate_layer=TestCandidateLayer(),
        styling_layer=TestStylingLayer(),
        method_layer=TestMultiDomainMethodLayer(),
    )

    pdf_techterms = techterm_layer.create_pdf_techterms(
        "test",
        PyPDFTermFixture.PDF_PATH,
        [
            DomainPDFList("test", [PyPDFTermFixture.PDF_PATH]),
            DomainPDFList("other", [WikipediaPDFFixture.PDF_PATH]),
        ],
    )

    PyPDFTermFixture.assert_pdf_techterms(pdf_techterms)


@mark.parametrize(
    "config",
    [
        TechnicalTermLayerConfig(max_num_terms=5, acceptance_rate=0.6),
        TechnicalTermLayerConfig(max_num_terms=1, acceptance_rate=0.1),
        TechnicalTermLayerConfig(max_num_terms=1, acceptance_rate=1.0),
    ],
)
def test_single_full_config_less(config: TechnicalTermLayerConfig) -> None:
    techterm_layer = SingleDomainTechnicalTermLayer(
        candidate_layer=TestCandidateLayer(),
        styling_layer=TestStylingLayer(),
        method_layer=TestSingleDomainMethodLayer(),
        config=config,
    )

    pdf_techterms = techterm_layer.create_pdf_techterms(
        PyPDFTermFixture.PDF_PATH, DomainPDFList("test", [PyPDFTermFixture.PDF_PATH])
    )

    raises(AssertionError, lambda: PyPDFTermFixture.assert_pdf_techterms(pdf_techterms))


@mark.parametrize(
    "config",
    [
        TechnicalTermLayerConfig(max_num_terms=10, acceptance_rate=1.0),
    ],
)
def test_single_full_config_more(config: TechnicalTermLayerConfig) -> None:
    techterm_layer = SingleDomainTechnicalTermLayer(
        candidate_layer=TestCandidateLayer(),
        styling_layer=TestStylingLayer(),
        method_layer=TestSingleDomainMethodLayer(),
        config=config,
    )

    pdf_techterms = techterm_layer.create_pdf_techterms(
        PyPDFTermFixture.PDF_PATH, DomainPDFList("test", [PyPDFTermFixture.PDF_PATH])
    )

    PyPDFTermFixture.assert_pdf_techterms(pdf_techterms)


@mark.parametrize(
    "config",
    [
        TechnicalTermLayerConfig(max_num_terms=5, acceptance_rate=0.6),
        TechnicalTermLayerConfig(max_num_terms=1, acceptance_rate=0.1),
        TechnicalTermLayerConfig(max_num_terms=1, acceptance_rate=1.0),
    ],
)
def test_multi_full_config_less(config: TechnicalTermLayerConfig) -> None:
    techterm_layer = MultiDomainTechnicalTermLayer(
        candidate_layer=TestCandidateLayer(),
        styling_layer=TestStylingLayer(),
        method_layer=TestMultiDomainMethodLayer(),
        config=config,
    )

    pdf_techterms = techterm_layer.create_pdf_techterms(
        "test",
        PyPDFTermFixture.PDF_PATH,
        [
            DomainPDFList("test", [PyPDFTermFixture.PDF_PATH]),
            DomainPDFList("other", [WikipediaPDFFixture.PDF_PATH]),
        ],
    )

    raises(AssertionError, lambda: PyPDFTermFixture.assert_pdf_techterms(pdf_techterms))


@mark.parametrize(
    "config",
    [
        TechnicalTermLayerConfig(max_num_terms=10, acceptance_rate=1.0),
    ],
)
def test_multi_full_config_more(config: TechnicalTermLayerConfig) -> None:
    techterm_layer = MultiDomainTechnicalTermLayer(
        candidate_layer=TestCandidateLayer(),
        styling_layer=TestStylingLayer(),
        method_layer=TestMultiDomainMethodLayer(),
        config=config,
    )

    pdf_techterms = techterm_layer.create_pdf_techterms(
        "test",
        PyPDFTermFixture.PDF_PATH,
        [
            DomainPDFList("test", [PyPDFTermFixture.PDF_PATH]),
            DomainPDFList("other", [WikipediaPDFFixture.PDF_PATH]),
        ],
    )

    PyPDFTermFixture.assert_pdf_techterms(pdf_techterms)


@mark.parametrize(
    "invalid_config, expected_exception",
    [
        (
            TechnicalTermLayerConfig(max_num_terms=0),
            ValueError,
        ),
        (
            TechnicalTermLayerConfig(acceptance_rate=0.0),
            ValueError,
        ),
        (
            TechnicalTermLayerConfig(acceptance_rate=1.1),
            ValueError,
        ),
    ],
)
def test_single_invalid_config(
    invalid_config: TechnicalTermLayerConfig, expected_exception: Type[Exception]
) -> None:
    raises(
        expected_exception,
        lambda: SingleDomainTechnicalTermLayer(
            candidate_layer=TestCandidateLayer(),
            styling_layer=TestStylingLayer(),
            method_layer=TestSingleDomainMethodLayer(),
            config=invalid_config,
        ),
    )


@mark.parametrize(
    "invalid_config, expected_exception",
    [
        (
            TechnicalTermLayerConfig(max_num_terms=0),
            ValueError,
        ),
        (
            TechnicalTermLayerConfig(acceptance_rate=0.0),
            ValueError,
        ),
        (
            TechnicalTermLayerConfig(acceptance_rate=1.1),
            ValueError,
        ),
    ],
)
def test_multi_invalid_config(
    invalid_config: TechnicalTermLayerConfig, expected_exception: Type[Exception]
) -> None:
    raises(
        expected_exception,
        lambda: MultiDomainTechnicalTermLayer(
            candidate_layer=TestCandidateLayer(),
            styling_layer=TestStylingLayer(),
            method_layer=TestMultiDomainMethodLayer(),
            config=invalid_config,
        ),
    )
