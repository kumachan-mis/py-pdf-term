from dataclasses import dataclass, field
from typing import List

from .base import BaseLayerConfig


@dataclass(frozen=True)
class CandidateLayerConfig(BaseLayerConfig):
    morpheme_filters: List[str] = field(
        default_factory=lambda: [
            "py_slides_term.JapaneseMorphemeFilter",
            "py_slides_term.EnglishMorphemeFilter",
        ]
    )
    term_filters: List[str] = field(
        default_factory=lambda: [
            "py_slides_term.JapaneseConcatenationFilter",
            "py_slides_term.EnglishConcatenationFilter",
            "py_slides_term.JapaneseSymbolLikeFilter",
            "py_slides_term.EnglishSymbolLikeFilter",
            "py_slides_term.JapaneseProperNounFilter",
            "py_slides_term.EnglishProperNounFilter",
            "py_slides_term.JapaneseNumericFilter",
            "py_slides_term.EnglishNumericFilter",
        ]
    )
    splitters: List[str] = field(
        default_factory=lambda: [
            "py_slides_term.SymbolNameSplitter",
            "py_slides_term.RepeatSplitter",
        ]
    )
    augmenters: List[str] = field(
        default_factory=lambda: [
            "py_slides_term.JapaneseModifyingParticleAugmenter",
            "py_slides_term.EnglishAdpositionAugmenter",
        ]
    )
    cache: str = "py_slides_term.CandidateLayerFileCache"
    remove_lower_layer_cache: bool = False
