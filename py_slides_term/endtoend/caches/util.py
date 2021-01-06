import json
from hashlib import sha256
from typing import List

from ..configs import BaseLayerConfig


def create_dir_name_from_config(config: BaseLayerConfig, prefix: str = "") -> str:
    return f"{prefix}{sha256(json.dumps(config.to_json()).encode()).hexdigest()}"


def create_file_name_from_path(file_path: str, ext: str, prefix: str = "") -> str:
    return f"{prefix}{sha256(file_path.encode()).hexdigest()}.{ext}"


def create_file_name_from_paths(
    file_paths: List[str], ext: str, prefix: str = ""
) -> str:
    sorted_paths = sorted(file_paths)
    return f"{prefix}{sha256(json.dumps(sorted_paths).encode()).hexdigest()}.{ext}"
