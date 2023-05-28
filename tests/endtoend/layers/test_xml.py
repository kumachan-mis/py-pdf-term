from pathlib import Path
from unittest.mock import ANY

from pytest import mark, raises
from pytest_mock import MockerFixture

from py_pdf_term.configs import XMLLayerConfig
from py_pdf_term.endtoend._endtoend.layers import XMLLayer
from py_pdf_term.endtoend.caches import XMLLayerNoCache
from py_pdf_term.mappers import BinaryOpenerMapper, XMLLayerCacheMapper
from py_pdf_term.pdftoxml import PDFtoXMLConverter
from py_pdf_term.pdftoxml.binopeners import StandardBinaryOpener

from ...fixtures import PyPDFTermFixture


class TestBinaryOpener(StandardBinaryOpener):
    __test__ = False


class TestXMLLayerCache(XMLLayerNoCache):
    __test__ = False


def test_minimal_config(tmp_path: Path) -> None:
    xml_layer = XMLLayer(cache_dir=tmp_path.as_posix())

    pdfnxml = xml_layer.create_pdfnxml(PyPDFTermFixture.PDF_PATH)

    PyPDFTermFixture.assert_pdfnxml(pdfnxml)


def test_full_config(tmp_path: Path, mocker: MockerFixture) -> None:
    spied_binary_open = mocker.spy(TestBinaryOpener, "open")
    spied_cache_load = mocker.spy(TestXMLLayerCache, "load")
    spied_cache_store = mocker.spy(TestXMLLayerCache, "store")

    config = XMLLayerConfig(
        bin_opener="test.TestBinaryOpener",
        include_pattern=r".*",
        exclude_pattern=r"py-pdf-term",
        nfc_norm=True,
        cache="test.TestXMLLayerCache",
    )
    bin_opener_mapper = BinaryOpenerMapper()
    bin_opener_mapper.add("test.TestBinaryOpener", TestBinaryOpener)
    cache_mapper = XMLLayerCacheMapper()
    cache_mapper.add("test.TestXMLLayerCache", TestXMLLayerCache)

    xml_layer = XMLLayer(
        config=config,
        bin_opener_mapper=bin_opener_mapper,
        cache_mapper=cache_mapper,
        cache_dir=tmp_path.as_posix(),
    )

    pdfnxml = xml_layer.create_pdfnxml(PyPDFTermFixture.PDF_PATH)

    assert pdfnxml.pdf_path == PyPDFTermFixture.PDF_PATH

    pages = list(pdfnxml.xml_root.iter("page"))
    assert len(pages) == 7

    assert pages[0].attrib["id"] == "1"
    assert len(list(pages[0])) == len(list(pages[0].iter("text")))
    assert pages[0].findtext("text") != "py-pdf-term"
    # py-pdf-term is excluded

    spied_binary_open.assert_called_once_with(ANY, PyPDFTermFixture.PDF_PATH, "rb")
    spied_cache_load.assert_called_once_with(ANY, PyPDFTermFixture.PDF_PATH, config)
    spied_cache_store.assert_called_once_with(ANY, pdfnxml, config)


def test_file_cache(tmp_path: Path, mocker: MockerFixture) -> None:
    spied_convert_as_element = mocker.spy(PDFtoXMLConverter, "convert_as_element")

    xml_layer = XMLLayer(cache_dir=tmp_path.as_posix())

    pdfnxml = xml_layer.create_pdfnxml(PyPDFTermFixture.PDF_PATH)

    assert spied_convert_as_element.call_count == 1
    PyPDFTermFixture.assert_pdfnxml(pdfnxml)

    assert spied_convert_as_element.call_count == 1
    PyPDFTermFixture.assert_pdfnxml(pdfnxml)

    xml_layer.remove_cache(PyPDFTermFixture.PDF_PATH)
    pdfnxml = xml_layer.create_pdfnxml(PyPDFTermFixture.PDF_PATH)

    assert spied_convert_as_element.call_count == 2
    PyPDFTermFixture.assert_pdfnxml(pdfnxml)


def test_no_cache(tmp_path: Path, mocker: MockerFixture) -> None:
    spied_convert_as_element = mocker.spy(PDFtoXMLConverter, "convert_as_element")

    xml_layer = XMLLayer(
        config=XMLLayerConfig(cache="py_pdf_term.XMLLayerNoCache"),
        cache_dir=tmp_path.as_posix(),
    )

    pdfnxml = xml_layer.create_pdfnxml(PyPDFTermFixture.PDF_PATH)

    assert spied_convert_as_element.call_count == 1
    PyPDFTermFixture.assert_pdfnxml(pdfnxml)

    pdfnxml = xml_layer.create_pdfnxml(PyPDFTermFixture.PDF_PATH)

    assert spied_convert_as_element.call_count == 2
    PyPDFTermFixture.assert_pdfnxml(pdfnxml)

    xml_layer.remove_cache(PyPDFTermFixture.PDF_PATH)
    pdfnxml = xml_layer.create_pdfnxml(PyPDFTermFixture.PDF_PATH)

    assert spied_convert_as_element.call_count == 3
    PyPDFTermFixture.assert_pdfnxml(pdfnxml)


@mark.parametrize(
    "invalid_config, expected_exception",
    [
        (
            XMLLayerConfig(bin_opener="py_pdf_term.UnknownBinaryOpener"),
            KeyError,
        ),
        (
            XMLLayerConfig(cache="py_pdf_term.UnknownXMLLayerCache"),
            KeyError,
        ),
    ],
)
def test_invalid_config(
    tmp_path: Path,
    invalid_config: XMLLayerConfig,
    expected_exception: type[Exception],
) -> None:
    raises(
        expected_exception,
        lambda: XMLLayer(config=invalid_config, cache_dir=tmp_path.as_posix()),
    )
