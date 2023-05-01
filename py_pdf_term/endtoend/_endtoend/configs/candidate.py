from dataclasses import dataclass, field
from typing import List

from .base import BaseLayerConfig


@dataclass(frozen=True)
class CandidateLayerConfig(BaseLayerConfig):
    """Configuration for candidate layer.

    Args
    ----
        lang_tokenizers:
            a list of language tokenizer class names. The default tokenizers are
            "py_pdf_term.JapaneseTokenizer" and "py_pdf_term.EnglishTokenizer".
        token_classifiers:
            a list of token classifier class names. The default classifiers are
            "py_pdf_term.JapaneseTokenClassifier" and
            "py_pdf_term.EnglishTokenClassifier".
        token_filters:
            a list of token filter class names. The default filters are
            "py_pdf_term.JapaneseTokenFilter" and "py_pdf_term.EnglishTokenFilter".
        term_filters:
            a list of term filter class names. The default filters are
            "py_pdf_term.JapaneseConcatenationFilter",
            "py_pdf_term.EnglishConcatenationFilter",
            "py_pdf_term.JapaneseSymbolLikeFilter",
            "py_pdf_term.EnglishSymbolLikeFilter",
            "py_pdf_term.JapaneseProperNounFilter",
            "py_pdf_term.EnglishProperNounFilter",
            "py_pdf_term.JapaneseNumericFilter", and
            "py_pdf_term.EnglishNumericFilter".
        splitters:
            a list of splitter class names. The default splitters are
            "py_pdf_term.SymbolNameSplitter" and "py_pdf_term.RepeatSplitter".
        augmenters:
            a list of augmenter class names. The default augmenters are
            "py_pdf_term.JapaneseAugmenter" and "py_pdf_term.EnglishAugmenter".
        cache:
            a cache class name. The default cache is
            "py_pdf_term.CandidateLayerFileCache".
    """

    lang_tokenizers: List[str] = field(
        default_factory=lambda: [
            "py_pdf_term.JapaneseTokenizer",
            "py_pdf_term.EnglishTokenizer",
        ]
    )
    token_classifiers: List[str] = field(
        default_factory=lambda: [
            "py_pdf_term.JapaneseTokenClassifier",
            "py_pdf_term.EnglishTokenClassifier",
        ]
    )
    token_filters: List[str] = field(
        default_factory=lambda: [
            "py_pdf_term.JapaneseTokenFilter",
            "py_pdf_term.EnglishTokenFilter",
        ]
    )
    term_filters: List[str] = field(
        default_factory=lambda: [
            "py_pdf_term.JapaneseConcatenationFilter",
            "py_pdf_term.EnglishConcatenationFilter",
            "py_pdf_term.JapaneseSymbolLikeFilter",
            "py_pdf_term.EnglishSymbolLikeFilter",
            "py_pdf_term.JapaneseProperNounFilter",
            "py_pdf_term.EnglishProperNounFilter",
            "py_pdf_term.JapaneseNumericFilter",
            "py_pdf_term.EnglishNumericFilter",
        ]
    )
    splitters: List[str] = field(
        default_factory=lambda: [
            "py_pdf_term.SymbolNameSplitter",
            "py_pdf_term.RepeatSplitter",
        ]
    )
    augmenters: List[str] = field(
        default_factory=lambda: [
            "py_pdf_term.JapaneseConnectorTermAugmenter",
            "py_pdf_term.EnglishConnectorTermAugmenter",
        ]
    )
    cache: str = "py_pdf_term.CandidateLayerFileCache"
