from typing import List, Dict, Any, Literal
from dataclasses import dataclass, asdict, field


@dataclass(frozen=True)
class BaseConfig:
    pass

    def to_json(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_json(cls, obj: Dict[str, Any]):
        return cls(**obj)


@dataclass(frozen=True)
class XMLConfig(BaseConfig):
    use_cache: bool = True


@dataclass(frozen=True)
class CandidateConfig(BaseConfig):
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


@dataclass(frozen=True)
class RankingMethodConfig(BaseConfig):
    method_type: Literal["single", "multi"] = "single"
    method: str = "py_slides_term.methods.MCValueMethod"
    hyper_params: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TechnicalTermConfig:
    max_num_pageterms: int = 14
    acceptance_rate: float = 0.9
