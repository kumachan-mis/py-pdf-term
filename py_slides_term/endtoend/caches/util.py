import json
from hashlib import sha256
from typing import List

from ..configs import BaseLayerConfig


def create_dir_name_from_config(config: BaseLayerConfig) -> str:
    return sha256(json.dumps(config.to_json()).encode()).hexdigest()


def create_file_name_from_path(file_path: str, ext: str) -> str:
    return f"{sha256(file_path.encode()).hexdigest()}.{ext}"


def create_file_name_from_paths(file_paths: List[str], ext: str) -> str:
    return f"{sha256(json.dumps(file_paths).encode()).hexdigest()}.{ext}"
