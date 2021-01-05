import os
import json
from typing import Union

from py_slides_term.candidates import PDFCandidateTermList
from .util import create_dir_name_from_config, create_file_name_from_path
from ..configs import CandidateLayerConfig


class CandidateLayerCache:
    def __init__(self, cache_dir: str):
        self._cache_dir = cache_dir

    def load(
        self, pdf_path: str, config: CandidateLayerConfig
    ) -> Union[PDFCandidateTermList, None]:
        dir_name = create_dir_name_from_config(config)
        file_name = create_file_name_from_path(pdf_path, "json")
        cache_file_path = os.path.join(self._cache_dir, dir_name, file_name)

        if not os.path.isfile(cache_file_path):
            return None

        with open(cache_file_path, "r") as json_file:
            obj = json.load(json_file)

        return PDFCandidateTermList.from_json(obj)

    def store(self, candidates: PDFCandidateTermList, config: CandidateLayerConfig):
        dir_name = create_dir_name_from_config(config)
        file_name = create_file_name_from_path(candidates.pdf_path, "json")
        cache_file_path = os.path.join(self._cache_dir, dir_name, file_name)

        os.makedirs(os.path.dirname(cache_file_path), exist_ok=True)

        with open(cache_file_path, "w") as json_file:
            json.dump(candidates.to_json(), json_file, ensure_ascii=False, indent=2)
