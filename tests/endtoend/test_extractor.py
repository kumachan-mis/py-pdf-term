from pathlib import Path

from pytest import mark, raises

from py_pdf_term import (
    DomainPDFList,
    PyPDFTermMultiDomainExtractor,
    PyPDFTermSingleDomainExtractor,
)
from py_pdf_term.configs import TechnicalTermLayerConfig

from ..fixtures import PyPDFTermFixture, WikipediaPDFFixture


def test_single_domain_extractor(tmp_path: Path) -> None:
    extractor = PyPDFTermSingleDomainExtractor(cache_dir=tmp_path.as_posix())

    pdf_techterms = extractor.extract(
        PyPDFTermFixture.PDF_PATH, DomainPDFList("test", [PyPDFTermFixture.PDF_PATH])
    )

    PyPDFTermFixture.assert_pdf_techterms(pdf_techterms)


def test_multi_domain_extractor(tmp_path: Path) -> None:
    extractor = PyPDFTermMultiDomainExtractor(
        techterm_config=TechnicalTermLayerConfig(max_num_terms=20),
        cache_dir=tmp_path.as_posix(),
    )

    pdf_techterms = extractor.extract(
        "test",
        PyPDFTermFixture.PDF_PATH,
        [
            DomainPDFList("test", [PyPDFTermFixture.PDF_PATH]),
            DomainPDFList("other", [WikipediaPDFFixture.PDF_PATH]),
        ],
    )

    PyPDFTermFixture.assert_pdf_techterms(pdf_techterms)


@mark.parametrize(
    "pdf_path, domain_pdf_list",
    [
        (
            "",
            DomainPDFList("test", [PyPDFTermFixture.PDF_PATH]),
        ),
        (
            PyPDFTermFixture.PDF_PATH,
            DomainPDFList("", [PyPDFTermFixture.PDF_PATH]),
        ),
        (
            PyPDFTermFixture.PDF_PATH,
            DomainPDFList("test", []),
        ),
        (
            PyPDFTermFixture.PDF_PATH,
            DomainPDFList("test", [WikipediaPDFFixture.PDF_PATH]),
        ),
    ],
)
def test_invalid_argument_single_domain_extractor(
    tmp_path: Path, pdf_path: str, domain_pdf_list: DomainPDFList
) -> None:
    extractor = PyPDFTermSingleDomainExtractor(cache_dir=tmp_path.as_posix())
    raises(ValueError, lambda: extractor.extract(pdf_path, domain_pdf_list))


@mark.parametrize(
    "domain, pdf_path, multi_domain_pdfs",
    [
        (
            "",
            PyPDFTermFixture.PDF_PATH,
            [
                DomainPDFList("test", [PyPDFTermFixture.PDF_PATH]),
                DomainPDFList("other", [WikipediaPDFFixture.PDF_PATH]),
            ],
        ),
        (
            "test",
            "",
            [
                DomainPDFList("test", [PyPDFTermFixture.PDF_PATH]),
                DomainPDFList("other", [WikipediaPDFFixture.PDF_PATH]),
            ],
        ),
        (
            "test",
            PyPDFTermFixture.PDF_PATH,
            [],
        ),
        (
            "test",
            PyPDFTermFixture.PDF_PATH,
            [
                DomainPDFList("test", [PyPDFTermFixture.PDF_PATH]),
            ],
        ),
        (
            "test",
            PyPDFTermFixture.PDF_PATH,
            [
                DomainPDFList("test", [PyPDFTermFixture.PDF_PATH]),
                DomainPDFList("", [WikipediaPDFFixture.PDF_PATH]),
            ],
        ),
        (
            "test",
            PyPDFTermFixture.PDF_PATH,
            [
                DomainPDFList("test", []),
                DomainPDFList("other", [WikipediaPDFFixture.PDF_PATH]),
            ],
        ),
        (
            "test",
            PyPDFTermFixture.PDF_PATH,
            [
                DomainPDFList("test", [PyPDFTermFixture.PDF_PATH]),
                DomainPDFList("other", []),
            ],
        ),
        (
            "test",
            PyPDFTermFixture.PDF_PATH,
            [
                DomainPDFList("test", [PyPDFTermFixture.PDF_PATH]),
                DomainPDFList("test", [WikipediaPDFFixture.PDF_PATH]),
            ],
        ),
        (
            "test",
            PyPDFTermFixture.PDF_PATH,
            [
                DomainPDFList("other", [PyPDFTermFixture.PDF_PATH]),
                DomainPDFList("another", [WikipediaPDFFixture.PDF_PATH]),
            ],
        ),
        (
            "test",
            PyPDFTermFixture.PDF_PATH,
            [
                DomainPDFList("test", [WikipediaPDFFixture.PDF_PATH]),
                DomainPDFList("other", [PyPDFTermFixture.PDF_PATH]),
            ],
        ),
    ],
)
def test_invalid_argument_multi_domain_extractor(
    tmp_path: Path, domain: str, pdf_path: str, multi_domain_pdfs: list[DomainPDFList]
) -> None:
    extractor = PyPDFTermMultiDomainExtractor(cache_dir=tmp_path.as_posix())
    raises(ValueError, lambda: extractor.extract(domain, pdf_path, multi_domain_pdfs))
