from os import path
from pathlib import Path

from py_pdf_term import (
    DomainPDFList,
    PyPDFTermMultiDomainExtractor,
    PyPDFTermSingleDomainExtractor,
)
from py_pdf_term.configs import TechnicalTermLayerConfig

FIXTURES_DIR = path.join(path.dirname(__file__), "..", "..", "test-fixtures")


def test_py_pdf_term_single_domain_extractor(tmp_path: Path):
    extractor = PyPDFTermSingleDomainExtractor(
        techterm_config=TechnicalTermLayerConfig(acceptance_rate=1.0),
        cache_dir=tmp_path.as_posix(),
    )
    pdf_path = path.join(FIXTURES_DIR, "py-pdf-term.pdf")

    terminologies = extractor.extract(pdf_path, DomainPDFList("test", [pdf_path]))

    assert terminologies.pdf_path == pdf_path

    assert len(terminologies.pages) == 7

    actual_terms = set(map(lambda t: t.term, terminologies.pages[0].terms))
    assert "py-pdf-term" in actual_terms

    actual_terms = set(map(lambda t: t.term, terminologies.pages[1].terms))
    assert "Motivation" in actual_terms

    actual_terms = set(map(lambda t: t.term, terminologies.pages[2].terms))
    assert "Features" in actual_terms

    actual_terms = set(map(lambda t: t.term, terminologies.pages[3].terms))
    assert "Features" in actual_terms

    actual_terms = set(map(lambda t: t.term, terminologies.pages[4].terms))
    assert "5-layers architecture" in actual_terms

    actual_terms = set(map(lambda t: t.term, terminologies.pages[5].terms))
    assert "5-layers architecture" in actual_terms

    actual_terms = set(map(lambda t: t.term, terminologies.pages[6].terms))
    assert "5-layers architecture" in actual_terms


def test_py_pdf_term_multi_domain_extractor(tmp_path: Path):
    extractor = PyPDFTermMultiDomainExtractor(
        techterm_config=TechnicalTermLayerConfig(acceptance_rate=1.0, max_num_terms=20),
        cache_dir=tmp_path.as_posix(),
    )
    pdf_path = path.join(FIXTURES_DIR, "py-pdf-term.pdf")

    terminologies = extractor.extract(
        "test",
        pdf_path,
        [DomainPDFList("test", [pdf_path]), DomainPDFList("other", [pdf_path])],
    )

    assert terminologies.pdf_path == pdf_path

    assert len(terminologies.pages) == 7

    actual_terms = set(map(lambda t: t.term, terminologies.pages[0].terms))
    assert "py-pdf-term" in actual_terms

    actual_terms = set(map(lambda t: t.term, terminologies.pages[1].terms))
    assert "Motivation" in actual_terms

    actual_terms = set(map(lambda t: t.term, terminologies.pages[2].terms))
    assert "Features" in actual_terms

    actual_terms = set(map(lambda t: t.term, terminologies.pages[3].terms))
    assert "Features" in actual_terms

    actual_terms = set(map(lambda t: t.term, terminologies.pages[4].terms))
    assert "5-layers architecture" in actual_terms

    actual_terms = set(map(lambda t: t.term, terminologies.pages[5].terms))
    assert "5-layers architecture" in actual_terms

    actual_terms = set(map(lambda t: t.term, terminologies.pages[6].terms))
    assert "5-layers architecture" in actual_terms
