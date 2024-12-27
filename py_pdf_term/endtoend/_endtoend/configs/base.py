from dataclasses import asdict, dataclass
from typing import Any

CACHE_CONFIGS = ["cache", "data_cache", "ranking_cache"]


@dataclass(frozen=True)
class BaseLayerConfig:
    """Base class for layer configuration."""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_dict_without_cache(self) -> dict[str, Any]:
        config_dict = asdict(self)
        for cache_config in CACHE_CONFIGS:
            config_dict.pop(cache_config, None)
        return config_dict

    @classmethod
    def from_dict[
        LayerConfig
    ](cls: type[LayerConfig], obj: dict[str, Any]) -> LayerConfig:
        return cls(**obj)
