import json
from hashlib import sha256

from ..configs import BaseLayerConfig


def create_dir_name(config: BaseLayerConfig) -> str:
    return sha256(json.dumps(config.to_json()).encode()).hexdigest()


def create_file_name(file_path: str, ext: str) -> str:
    return f"{sha256(file_path.encode()).hexdigest()}.{ext}"
