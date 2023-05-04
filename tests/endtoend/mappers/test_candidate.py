from py_pdf_term.mappers import (
    AugmenterMapper,
    CandidateTokenFilterMapper,
    CandidateTermFilterMapper,
    LanguageTokenizerMapper,
    SplitterMapper,
    TokenClassifierMapper,
)
from py_pdf_term.candidates.augmenters import (
    JapaneseConnectorTermAugmenter,
    EnglishConnectorTermAugmenter,
)
from py_pdf_term.candidates.filters import (
    JapaneseTokenFilter,
    EnglishTokenFilter,
    JapaneseConcatenationFilter,
    EnglishConcatenationFilter,
    JapaneseSymbolLikeFilter,
    EnglishSymbolLikeFilter,
    JapaneseProperNounFilter,
    EnglishProperNounFilter,
    JapaneseNumericFilter,
    EnglishNumericFilter,
)
from py_pdf_term.candidates.splitters import (
    SymbolNameSplitter,
    RepeatSplitter,
)
from py_pdf_term.tokenizers import JapaneseTokenizer, EnglishTokenizer
from py_pdf_term.candidates.classifiers import (
    JapaneseTokenClassifier,
    EnglishTokenClassifier,
)


def test_language_tokenizer_default_mapper() -> None:
    mapper = LanguageTokenizerMapper.default_mapper()

    clses = mapper.bulk_find_or_none(
        [
            "py_pdf_term.JapaneseTokenizer",
            "py_pdf_term.EnglishTokenizer",
            "py_pdf_term.UnknownTokenizer",
        ]
    )
    assert clses == [JapaneseTokenizer, EnglishTokenizer, None]


def test_token_classifier_default_mapper() -> None:
    mapper = TokenClassifierMapper.default_mapper()

    clses = mapper.bulk_find_or_none(
        [
            "py_pdf_term.JapaneseTokenClassifier",
            "py_pdf_term.EnglishTokenClassifier",
            "py_pdf_term.UnknownTokenClassifier",
        ]
    )
    assert clses == [JapaneseTokenClassifier, EnglishTokenClassifier, None]


def test_candidate_token_filter_default_mapper() -> None:
    mapper = CandidateTokenFilterMapper.default_mapper()

    clses = mapper.bulk_find_or_none(
        [
            "py_pdf_term.JapaneseTokenFilter",
            "py_pdf_term.EnglishTokenFilter",
            "py_pdf_term.UnknownTokenFilter",
        ]
    )
    assert clses == [JapaneseTokenFilter, EnglishTokenFilter, None]


def test_candidate_term_filter_default_mapper() -> None:
    mapper = CandidateTermFilterMapper.default_mapper()

    clses = mapper.bulk_find_or_none(
        [
            "py_pdf_term.JapaneseConcatenationFilter",
            "py_pdf_term.EnglishConcatenationFilter",
            "py_pdf_term.JapaneseSymbolLikeFilter",
            "py_pdf_term.EnglishSymbolLikeFilter",
            "py_pdf_term.JapaneseProperNounFilter",
            "py_pdf_term.EnglishProperNounFilter",
            "py_pdf_term.JapaneseNumericFilter",
            "py_pdf_term.EnglishNumericFilter",
            "py_pdf_term.UnknownTermFilter",
        ]
    )
    assert clses == [
        JapaneseConcatenationFilter,
        EnglishConcatenationFilter,
        JapaneseSymbolLikeFilter,
        EnglishSymbolLikeFilter,
        JapaneseProperNounFilter,
        EnglishProperNounFilter,
        JapaneseNumericFilter,
        EnglishNumericFilter,
        None,
    ]


def test_splitter_default_mapper() -> None:
    mapper = SplitterMapper.default_mapper()

    clses = mapper.bulk_find_or_none(
        [
            "py_pdf_term.SymbolNameSplitter",
            "py_pdf_term.RepeatSplitter",
            "py_pdf_term.UnknownSplitter",
        ]
    )
    assert clses == [SymbolNameSplitter, RepeatSplitter, None]


def test_augmenter_default_mapper() -> None:
    mapper = AugmenterMapper.default_mapper()

    clses = mapper.bulk_find_or_none(
        [
            "py_pdf_term.JapaneseConnectorTermAugmenter",
            "py_pdf_term.EnglishConnectorTermAugmenter",
            "py_pdf_term.UnknownAugmenter",
        ]
    )
    assert clses == [
        JapaneseConnectorTermAugmenter,
        EnglishConnectorTermAugmenter,
        None,
    ]
