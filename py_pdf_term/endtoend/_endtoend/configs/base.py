from dataclasses import asdict, dataclass
from typing import Any, Dict, Type, TypeVar

CACHE_CONFIGS = ["cache", "data_cache", "ranking_cache"]


@dataclass(frozen=True)
class BaseLayerConfig:
    pass

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_dict_without_cache(self) -> Dict[str, Any]:
        config_dict = asdict(self)
        for cache_config in CACHE_CONFIGS:
            config_dict.pop(cache_config, None)
        return config_dict

    @classmethod
    def from_dict(cls: Type["LayerConfig"], obj: Dict[str, Any]) -> "LayerConfig":
        return cls(**obj)


LayerConfig = TypeVar("LayerConfig", bound=BaseLayerConfig)
