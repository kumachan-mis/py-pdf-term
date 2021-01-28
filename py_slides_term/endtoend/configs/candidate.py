from dataclasses import dataclass, field
from typing import List

from .base import BaseLayerConfig


@dataclass(frozen=True)
class CandidateLayerConfig(BaseLayerConfig):
    morpheme_filters: List[str] = field(
        default_factory=lambda: [
            "py_slides_term.candidates.JapaneseMorphemeFilter",
            "py_slides_term.candidates.EnglishMorphemeFilter",
        ]
    )
    term_filters: List[str] = field(
        default_factory=lambda: [
            "py_slides_term.candidates.JapaneseConcatenationFilter",
            "py_slides_term.candidates.EnglishConcatenationFilter",
            "py_slides_term.candidates.JapaneseSymbolLikeFilter",
            "py_slides_term.candidates.EnglishSymbolLikeFilter",
            "py_slides_term.candidates.JapaneseProperNounFilter",
            "py_slides_term.candidates.EnglishProperNounFilter",
        ]
    )
    modifying_particle_augmentation: bool = True
    use_cache: bool = True
    remove_lower_layer_cache: bool = True
