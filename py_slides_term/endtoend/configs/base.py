from typing import Dict, Any, Type, TypeVar
from dataclasses import dataclass, asdict

CACHE_CONFIGS = ["use_cache", "remove_lower_layer_cache"]


@dataclass(frozen=True)
class BaseLayerConfig:
    pass

    def to_json(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json_without_cache(self) -> Dict[str, Any]:
        config_dict = asdict(self)
        for cache_config in CACHE_CONFIGS:
            config_dict.pop(cache_config, None)
        return config_dict

    @classmethod
    def from_json(cls: Type["LayerConfig"], obj: Dict[str, Any]) -> "LayerConfig":
        return cls(**obj)


LayerConfig = TypeVar("LayerConfig", bound=BaseLayerConfig)
