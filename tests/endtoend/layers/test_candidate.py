from pathlib import Path
from typing import List, Optional, Type
from xml.etree.ElementTree import parse

from pytest import mark, raises
from pytest_mock import MockerFixture

from py_pdf_term import DomainPDFList
from py_pdf_term.candidates import CandidateTermExtractor
from py_pdf_term.candidates.augmenters import BaseAugmenter
from py_pdf_term.candidates.classifiers import EnglishTokenClassifier
from py_pdf_term.candidates.filters import (
    BaseEnglishCandidateTermFilter,
    EnglishTokenFilter,
)
from py_pdf_term.candidates.splitters import BaseSplitter
from py_pdf_term.configs import CandidateLayerConfig
from py_pdf_term.endtoend._endtoend.layers import CandidateLayer, XMLLayer
from py_pdf_term.endtoend.caches import CandidateLayerNoCache
from py_pdf_term.mappers import (
    AugmenterMapper,
    CandidateLayerCacheMapper,
    CandidateTermFilterMapper,
    CandidateTokenFilterMapper,
    LanguageTokenizerMapper,
    SplitterMapper,
    TokenClassifierMapper,
)
from py_pdf_term.pdftoxml import PDFnXMLElement
from py_pdf_term.tokenizers import EnglishTokenizer, Term, Token

from ...fixtures import PyPDFTermFixture


class TestXMLLayer(XMLLayer):
    __test__ = False

    def create_pdfnxml(self, pdf_path: str) -> PDFnXMLElement:
        xml_root = parse(PyPDFTermFixture.XML_PATH).getroot()
        return PDFnXMLElement(pdf_path, xml_root)

    def remove_cache(self, pdf_path: str) -> None:
        pass


class TestTokenizer(EnglishTokenizer):
    __test__ = False


class TestTokenClassifier(EnglishTokenClassifier):
    __test__ = False


class TestCandidateTokenFilter(EnglishTokenFilter):
    __test__ = False

    def is_partof_candidate(self, tokens: List[Token], idx: int) -> bool:
        return str(tokens[idx]) != "architecture"


class TestCandidateTermFilter(BaseEnglishCandidateTermFilter):
    __test__ = False

    def is_candidate(self, scoped_term: Term) -> bool:
        return str(scoped_term) != "Features"


class TestSplitter(BaseSplitter):
    __test__ = False

    def split(self, term: Term) -> List[Term]:
        if term.tokens and str(term.tokens[-1]) == "Layer":
            return [
                Term(term.tokens[:-1], term.fontsize, term.ncolor, term.augmented),
                Term(term.tokens[-1:], term.fontsize, term.ncolor, term.augmented),
            ]
        return [term]


class TestAugmenter(BaseAugmenter):
    __test__ = False

    def augment(self, term: Term) -> List[Term]:
        if term.tokens and str(term.tokens[-1]) == "use":
            return [
                Term(term.tokens[:-1], term.fontsize, term.ncolor, term.augmented),
                Term(term.tokens[-1:], term.fontsize, term.ncolor, term.augmented),
            ]
        return []


class TestCandidateLayerCache(CandidateLayerNoCache):
    __test__ = False


def test_minimal_config(tmp_path: Path) -> None:
    xml_layer = TestXMLLayer(cache_dir=tmp_path.as_posix())
    candidate_layer = CandidateLayer(xml_layer=xml_layer, cache_dir=tmp_path.as_posix())
    domain_pdfs = DomainPDFList("test", [PyPDFTermFixture.PDF_PATH])

    domain_candidates = candidate_layer.create_domain_candidates(domain_pdfs)

    assert domain_candidates.domain == "test"
    assert len(domain_candidates.pdfs) == 1
    PyPDFTermFixture.assert_pdf_candidates(domain_candidates.pdfs[0])


def test_full_config(tmp_path: Path) -> None:
    xml_layer = TestXMLLayer(cache_dir=tmp_path.as_posix())

    config = CandidateLayerConfig(
        lang_tokenizers=["test.TestTokenizer"],
        token_classifiers=["test.TestTokenClassifier"],
        token_filters=[
            "py_pdf_term.EnglishTokenFilter",
            "test.TestCandidateTokenFilter",
        ],
        term_filters=[
            "py_pdf_term.EnglishConcatenationFilter",
            "py_pdf_term.EnglishSymbolLikeFilter",
            "py_pdf_term.EnglishProperNounFilter",
            "py_pdf_term.EnglishNumericFilter",
            "test.TestCandidateTermFilter",
        ],
        splitters=[
            "py_pdf_term.SymbolNameSplitter",
            "py_pdf_term.RepeatSplitter",
            "test.TestSplitter",
        ],
        augmenters=[
            "py_pdf_term.EnglishConnectorTermAugmenter",
            "test.TestAugmenter",
        ],
        cache="test.TestCandidateLayerCache",
    )
    lang_tokenizer_mapper = LanguageTokenizerMapper()
    lang_tokenizer_mapper.add("test.TestTokenizer", TestTokenizer)
    token_classifier_mapper = TokenClassifierMapper()
    token_classifier_mapper.add("test.TestTokenClassifier", TestTokenClassifier)
    token_filter_mapper = CandidateTokenFilterMapper.default_mapper()
    token_filter_mapper.add("test.TestCandidateTokenFilter", TestCandidateTokenFilter)
    term_filter_mapper = CandidateTermFilterMapper.default_mapper()
    term_filter_mapper.add("test.TestCandidateTermFilter", TestCandidateTermFilter)
    splitter_mapper = SplitterMapper.default_mapper()
    splitter_mapper.add("test.TestSplitter", TestSplitter)
    augmenter_mapper = AugmenterMapper.default_mapper()
    augmenter_mapper.add("test.TestAugmenter", TestAugmenter)
    cache_mapper = CandidateLayerCacheMapper()
    cache_mapper.add("test.TestCandidateLayerCache", TestCandidateLayerCache)

    candidate_layer = CandidateLayer(
        xml_layer=xml_layer,
        config=config,
        lang_tokenizer_mapper=lang_tokenizer_mapper,
        token_classifier_mapper=token_classifier_mapper,
        token_filter_mapper=token_filter_mapper,
        term_filter_mapper=term_filter_mapper,
        splitter_mapper=splitter_mapper,
        augmenter_mapper=augmenter_mapper,
        cache_mapper=cache_mapper,
        cache_dir=tmp_path.as_posix(),
    )
    domain_pdfs = DomainPDFList("test", [PyPDFTermFixture.PDF_PATH])

    domain_candidates = candidate_layer.create_domain_candidates(domain_pdfs)

    def find_candidate_by_text(text: str, candidates: List[Term]) -> Optional[Term]:
        return next(filter(lambda t: str(t) == text, candidates), None)

    assert domain_candidates.domain == "test"
    assert len(domain_candidates.pdfs) == 1

    pdf_candidates = domain_candidates.pdfs[0]

    assert pdf_candidates.pdf_path == PyPDFTermFixture.PDF_PATH
    assert len(pdf_candidates.pages) == 7

    candidates = pdf_candidates.pages[0]
    assert candidates.page_num == 1

    term = find_candidate_by_text("py-pdf-term", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 52.000) < 0.001
    assert term.ncolor == "(0.0, 0.0, 0.0)"

    term = find_candidate_by_text("Python", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 21.700) < 0.001
    assert term.ncolor == "(0.34901962, 0.34901962, 0.34901962)"

    candidates = pdf_candidates.pages[1]
    assert candidates.page_num == 2

    term = find_candidate_by_text("Motivation", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 25.200) < 0.001
    assert term.ncolor == "(0.0, 0.0, 0.0)"

    term = find_candidate_by_text("practical use", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 20.000) < 0.001
    assert term.ncolor == "(1.0, 0.0, 0.0)"

    term = find_candidate_by_text("practical", candidates.candidates)
    assert term is None
    # "practical" is not a candidate because it is a noun

    term = find_candidate_by_text("use", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 20.000) < 0.001
    assert term.ncolor == "(1.0, 0.0, 0.0)"
    # "use" is a candidate because it is augmented by TestAugmenter and
    # is a noun in this context

    candidates = pdf_candidates.pages[2]
    assert candidates.page_num == 3

    term = find_candidate_by_text("laboratory use", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 25.200) < 0.001
    assert term.ncolor == "(0.0, 0.0, 0.0)"

    term = find_candidate_by_text("laboratory", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 25.200) < 0.001
    assert term.ncolor == "(0.0, 0.0, 0.0)"

    term = find_candidate_by_text("use", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 25.200) < 0.001
    assert term.ncolor == "(0.0, 0.0, 0.0)"
    # "use" is a candidate because it is augmented by TestAugmenter and
    # is a noun in this context

    term = find_candidate_by_text("ranking algorithms", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 20.000) < 0.001
    assert term.ncolor == "(0.34901962, 0.34901962, 0.34901962)"

    candidates = pdf_candidates.pages[3]
    assert candidates.page_num == 4

    term = find_candidate_by_text("practical use", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 25.200) < 0.001
    assert term.ncolor == "(0.0, 0.0, 0.0)"

    term = find_candidate_by_text("practical", candidates.candidates)
    assert term is None
    # "practical" is not a candidate because it is a noun

    term = find_candidate_by_text("use", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 25.200) < 0.001
    assert term.ncolor == "(0.0, 0.0, 0.0)"
    # "use" is a candidate because it is augmented by TestAugmenter and
    # is a noun in this context

    term = find_candidate_by_text("cache mechanism", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 20.000) < 0.001
    assert term.ncolor == "(0.34901962, 0.34901962, 0.34901962)"

    candidates = pdf_candidates.pages[4]
    assert candidates.page_num == 5

    term = find_candidate_by_text("XML Layer", candidates.candidates)
    assert term is None
    # "XML Layer" is split by TestSplitter

    term = find_candidate_by_text("XML", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 0.0) < 0.001
    assert term.ncolor == "(0.0, 0.0, 0.0)"

    term = find_candidate_by_text("Layer", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 0.0) < 0.001
    assert term.ncolor == "(0.0, 0.0, 0.0)"

    term = find_candidate_by_text("Candidate Term Layer", candidates.candidates)
    assert term is None
    # "Candidate Term Layer" is split by TestSplitter

    term = find_candidate_by_text("Candidate Term", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 0.0) < 0.001
    assert term.ncolor == "(0.0, 0.0, 0.0)"

    term = find_candidate_by_text("Layer", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 0.0) < 0.001
    assert term.ncolor == "(0.0, 0.0, 0.0)"

    candidates = pdf_candidates.pages[5]
    assert candidates.page_num == 6

    term = find_candidate_by_text("Method Layer", candidates.candidates)
    assert term is None
    # "Method Layer" is split by TestSplitter

    term = find_candidate_by_text("Method", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 0.0) < 0.001
    assert term.ncolor == "(0.0, 0.0, 0.0)"

    term = find_candidate_by_text("Layer", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 0.0) < 0.001
    assert term.ncolor == "(0.0, 0.0, 0.0)"

    term = find_candidate_by_text("Styling Layer", candidates.candidates)
    assert term is None
    # "Styling Layer" is split by TestSplitter

    term = find_candidate_by_text("Styling", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 0.0) < 0.001
    assert term.ncolor == "(0.0, 0.0, 0.0)"

    term = find_candidate_by_text("Layer", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 0.0) < 0.001
    assert term.ncolor == "(0.0, 0.0, 0.0)"

    candidates = pdf_candidates.pages[6]
    assert candidates.page_num == 7

    term = find_candidate_by_text("Technical Term Layer", candidates.candidates)
    assert term is None
    # "Technical Term Layer" is split by TestSplitter

    term = find_candidate_by_text("Technical Term", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 0.0) < 0.001
    assert term.ncolor == "(0.0, 0.0, 0.0)"

    term = find_candidate_by_text("Layer", candidates.candidates)
    assert term is not None
    assert abs(term.fontsize - 0.0) < 0.001
    assert term.ncolor == "(0.0, 0.0, 0.0)"


def test_file_cache(tmp_path: Path, mocker: MockerFixture) -> None:
    spied_extract_from_xml_element = mocker.spy(
        CandidateTermExtractor, "extract_from_xml_element"
    )

    xml_layer = TestXMLLayer(cache_dir=tmp_path.as_posix())
    candidate_layer = CandidateLayer(xml_layer=xml_layer, cache_dir=tmp_path.as_posix())
    domain_pdfs = DomainPDFList("test", [PyPDFTermFixture.PDF_PATH])

    domain_candidates = candidate_layer.create_domain_candidates(domain_pdfs)

    assert spied_extract_from_xml_element.call_count == 1
    assert domain_candidates.domain == "test"
    assert len(domain_candidates.pdfs) == 1
    PyPDFTermFixture.assert_pdf_candidates(domain_candidates.pdfs[0])

    domain_candidates = candidate_layer.create_domain_candidates(domain_pdfs)

    assert spied_extract_from_xml_element.call_count == 1
    assert domain_candidates.domain == "test"
    assert len(domain_candidates.pdfs) == 1
    PyPDFTermFixture.assert_pdf_candidates(domain_candidates.pdfs[0])

    candidate_layer.remove_cache(PyPDFTermFixture.PDF_PATH)
    domain_candidates = candidate_layer.create_domain_candidates(domain_pdfs)

    assert spied_extract_from_xml_element.call_count == 2
    assert domain_candidates.domain == "test"
    assert len(domain_candidates.pdfs) == 1
    PyPDFTermFixture.assert_pdf_candidates(domain_candidates.pdfs[0])


def test_no_cache(tmp_path: Path, mocker: MockerFixture) -> None:
    spied_extract_from_xml_element = mocker.spy(
        CandidateTermExtractor, "extract_from_xml_element"
    )

    xml_layer = TestXMLLayer(cache_dir=tmp_path.as_posix())
    candidate_layer = CandidateLayer(
        xml_layer=xml_layer,
        config=CandidateLayerConfig(cache="py_pdf_term.CandidateLayerNoCache"),
        cache_dir=tmp_path.as_posix(),
    )
    domain_pdfs = DomainPDFList("test", [PyPDFTermFixture.PDF_PATH])

    domain_candidates = candidate_layer.create_domain_candidates(domain_pdfs)

    assert spied_extract_from_xml_element.call_count == 1
    assert domain_candidates.domain == "test"
    assert len(domain_candidates.pdfs) == 1
    PyPDFTermFixture.assert_pdf_candidates(domain_candidates.pdfs[0])

    domain_candidates = candidate_layer.create_domain_candidates(domain_pdfs)

    assert spied_extract_from_xml_element.call_count == 2
    assert domain_candidates.domain == "test"
    assert len(domain_candidates.pdfs) == 1
    PyPDFTermFixture.assert_pdf_candidates(domain_candidates.pdfs[0])

    candidate_layer.remove_cache(PyPDFTermFixture.PDF_PATH)
    domain_candidates = candidate_layer.create_domain_candidates(domain_pdfs)

    assert spied_extract_from_xml_element.call_count == 3
    assert domain_candidates.domain == "test"
    assert len(domain_candidates.pdfs) == 1
    PyPDFTermFixture.assert_pdf_candidates(domain_candidates.pdfs[0])


@mark.parametrize(
    "invalid_config,expected_exception",
    [
        (
            CandidateLayerConfig(lang_tokenizers=["py_pdf_term.UnknownTokenizer"]),
            KeyError,
        ),
        (
            CandidateLayerConfig(token_classifiers=["py_pdf_term.UnknownClassifier"]),
            KeyError,
        ),
        (
            CandidateLayerConfig(token_filters=["py_pdf_term.UnknownTokenFilter"]),
            KeyError,
        ),
        (
            CandidateLayerConfig(term_filters=["py_pdf_term.UnknownTermFilter"]),
            KeyError,
        ),
        (
            CandidateLayerConfig(splitters=["py_pdf_term.UnknownSplitter"]),
            KeyError,
        ),
        (
            CandidateLayerConfig(augmenters=["py_pdf_term.UnknownAugmenter"]),
            KeyError,
        ),
        (
            CandidateLayerConfig(cache="py_pdf_term.UnknownCandidateLayerCache"),
            KeyError,
        ),
    ],
)
def test_invalid_config(
    tmp_path: Path,
    invalid_config: CandidateLayerConfig,
    expected_exception: Type[Exception],
) -> None:
    xml_layer = TestXMLLayer(cache_dir=tmp_path.as_posix())
    raises(
        expected_exception,
        lambda: CandidateLayer(
            xml_layer=xml_layer, config=invalid_config, cache_dir=tmp_path.as_posix()
        ),
    )
