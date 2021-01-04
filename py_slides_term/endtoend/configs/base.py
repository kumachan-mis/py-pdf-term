from typing import Dict, Any
from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class BaseLayerConfig:
    pass

    def to_json(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_json(cls, obj: Dict[str, Any]):
        return cls(**obj)
