import json
from hashlib import sha256
from typing import List

from ..configs import BaseLayerConfig


def create_dir_name_from_config(config: BaseLayerConfig, prefix: str = "") -> str:
    config_class_name = config.__class__.__name__
    config_json = json.dumps(config.to_dict_without_cache())
    return f"{prefix}{sha256((config_class_name + config_json).encode()).hexdigest()}"


def create_file_name_from_path(path: str, ext: str, prefix: str = "") -> str:
    return f"{prefix}{sha256(path.encode()).hexdigest()}.{ext}"


def create_file_name_from_paths(paths: List[str], ext: str, prefix: str = "") -> str:
    return f"{prefix}{sha256(json.dumps(sorted(paths)).encode()).hexdigest()}.{ext}"
