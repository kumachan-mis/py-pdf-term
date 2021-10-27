from dataclasses import dataclass, field
from typing import List

from .base import BaseLayerConfig


@dataclass(frozen=True)
class CandidateLayerConfig(BaseLayerConfig):
    lang_tokenizers: List[str] = field(
        default_factory=lambda: [
            "py_pdf_term.JapaneseTokenizer",
            "py_pdf_term.EnglishTokenizer",
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
            "py_pdf_term.JapaneseModifyingParticleAugmenter",
            "py_pdf_term.EnglishAdpositionAugmenter",
        ]
    )
    cache: str = "py_pdf_term.CandidateLayerFileCache"
