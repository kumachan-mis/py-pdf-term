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
            "py_slides_term.candidates.ConcatenationFilter",
            "py_slides_term.candidates.SymbolLikeFilter",
            "py_slides_term.candidates.ProperNounFilter",
        ]
    )
    modifying_particle_augmentation: bool = False
    use_cache: bool = True
    remove_lower_layer_cache: bool = True
