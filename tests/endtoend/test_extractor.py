from pathlib import Path

from py_pdf_term import (
    DomainPDFList,
    PyPDFTermMultiDomainExtractor,
    PyPDFTermSingleDomainExtractor,
)
from py_pdf_term.configs import TechnicalTermLayerConfig

from ..fixtures import PyPDFTermFixture


def test_py_pdf_term_single_domain_extractor(tmp_path: Path):
    extractor = PyPDFTermSingleDomainExtractor(
        techterm_config=TechnicalTermLayerConfig(acceptance_rate=1.0),
        cache_dir=tmp_path.as_posix(),
    )

    pdf_techterms = extractor.extract(
        PyPDFTermFixture.PDF_PATH, DomainPDFList("test", [PyPDFTermFixture.PDF_PATH])
    )

    PyPDFTermFixture.assert_pdf_techterms(pdf_techterms)


def test_py_pdf_term_multi_domain_extractor(tmp_path: Path):
    extractor = PyPDFTermMultiDomainExtractor(
        techterm_config=TechnicalTermLayerConfig(acceptance_rate=1.0, max_num_terms=20),
        cache_dir=tmp_path.as_posix(),
    )

    pdf_techterms = extractor.extract(
        "test",
        PyPDFTermFixture.PDF_PATH,
        [
            DomainPDFList("test", [PyPDFTermFixture.PDF_PATH]),
            DomainPDFList("other", [PyPDFTermFixture.PDF_PATH]),
        ],
    )

    PyPDFTermFixture.assert_pdf_techterms(pdf_techterms)
