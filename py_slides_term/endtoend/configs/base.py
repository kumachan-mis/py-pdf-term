from typing import Dict, Any, Type, TypeVar
from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class BaseLayerConfig:
    pass

    def to_json(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_json(cls: Type["LayerConfig"], obj: Dict[str, Any]) -> "LayerConfig":
        return cls(**obj)


LayerConfig = TypeVar("LayerConfig", bound=BaseLayerConfig)
