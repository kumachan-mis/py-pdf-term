import json
import os
from glob import glob
from shutil import rmtree
from typing import Any, Callable, Dict, List, Union

from py_pdf_term.methods import MethodTermRanking
from py_pdf_term.methods._methods.rankingdata import RankingData

from ...configs import MethodLayerConfig
from ..util import create_dir_name_from_config, create_file_name_from_paths
from .base import BaseMethodLayerDataCache, BaseMethodLayerRankingCache


class MethodLayerRankingFileCache(BaseMethodLayerRankingCache):
    def __init__(self, cache_dir: str) -> None:
        super().__init__(cache_dir)
        self._cache_dir = cache_dir

    def load(
        self,
        pdf_paths: List[str],
        config: MethodLayerConfig,
    ) -> Union[MethodTermRanking, None]:
        dir_name = create_dir_name_from_config(config, prefix="rank")
        file_name = create_file_name_from_paths(pdf_paths, "json")
        cache_file_path = os.path.join(self._cache_dir, dir_name, file_name)

        if not os.path.isfile(cache_file_path):
            return None

        with open(cache_file_path, "r") as json_file:
            try:
                obj = json.load(json_file)
            except json.JSONDecodeError:
                return None

        return MethodTermRanking.from_dict(obj)

    def store(
        self,
        pdf_paths: List[str],
        term_ranking: MethodTermRanking,
        config: MethodLayerConfig,
    ) -> None:
        dir_name = create_dir_name_from_config(config, prefix="rank")
        file_name = create_file_name_from_paths(pdf_paths, "json")
        cache_file_path = os.path.join(self._cache_dir, dir_name, file_name)

        os.makedirs(os.path.dirname(cache_file_path), exist_ok=True)

        with open(cache_file_path, "w") as json_file:
            json.dump(term_ranking.to_dict(), json_file, ensure_ascii=False, indent=2)

    def remove(self, pdf_paths: List[str], config: MethodLayerConfig) -> None:
        dir_name = create_dir_name_from_config(config, prefix="rank")
        file_name = create_file_name_from_paths(pdf_paths, "json")
        cache_dir_path = os.path.join(self._cache_dir, dir_name)
        cache_file_path = os.path.join(cache_dir_path, file_name)

        if not os.path.isfile(cache_file_path):
            return

        os.remove(cache_file_path)

        cache_file_paths = glob(os.path.join(cache_dir_path, "*.json"))
        if not cache_file_paths:
            rmtree(cache_dir_path)


class MethodLayerDataFileCache(BaseMethodLayerDataCache[RankingData]):
    def __init__(self, cache_dir: str) -> None:
        super().__init__(cache_dir)
        self._cache_dir = cache_dir

    def load(
        self,
        pdf_paths: List[str],
        config: MethodLayerConfig,
        from_dict: Callable[[Dict[str, Any]], RankingData],
    ) -> Union[RankingData, None]:
        dir_name = create_dir_name_from_config(config, prefix="data")
        file_name = create_file_name_from_paths(pdf_paths, "json")
        cache_file_path = os.path.join(self._cache_dir, dir_name, file_name)

        if not os.path.isfile(cache_file_path):
            return None

        with open(cache_file_path, "r") as json_file:
            obj = json.load(json_file)

        return from_dict(obj)

    def store(
        self,
        pdf_paths: List[str],
        ranking_data: RankingData,
        config: MethodLayerConfig,
    ) -> None:
        dir_name = create_dir_name_from_config(config, prefix="data")
        file_name = create_file_name_from_paths(pdf_paths, "json")
        cache_file_path = os.path.join(self._cache_dir, dir_name, file_name)

        os.makedirs(os.path.dirname(cache_file_path), exist_ok=True)

        with open(cache_file_path, "w") as json_file:
            json.dump(ranking_data.to_dict(), json_file, ensure_ascii=False, indent=2)

    def remove(self, pdf_paths: List[str], config: MethodLayerConfig) -> None:
        dir_name = create_dir_name_from_config(config, prefix="data")
        file_name = create_file_name_from_paths(pdf_paths, "json")
        cache_dir_path = os.path.join(self._cache_dir, dir_name)
        cache_file_path = os.path.join(cache_dir_path, file_name)

        if not os.path.isfile(cache_file_path):
            return

        os.remove(cache_file_path)

        cache_file_paths = glob(os.path.join(cache_dir_path, "*.json"))
        if not cache_file_paths:
            rmtree(cache_dir_path)
