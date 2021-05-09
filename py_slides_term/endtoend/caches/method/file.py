import os
import json
from glob import glob
from shutil import rmtree
from typing import List, Dict, Any, Union, Callable

from .base import BaseMethodLayerRankingCache, BaseMethodLayerDataCache
from ...configs import MethodLayerConfig
from ..util import create_dir_name_from_config, create_file_name_from_paths
from py_slides_term.methods import DomainTermRanking
from py_slides_term.methods.rankingdata import RankingData


class MethodLayerRankingFileCache(BaseMethodLayerRankingCache):
    # public
    def __init__(self, cache_dir: str):
        super().__init__(cache_dir)
        self._cache_dir = cache_dir

    def load(
        self,
        pdf_paths: List[str],
        config: MethodLayerConfig,
    ) -> Union[DomainTermRanking, None]:
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

        return DomainTermRanking.from_json(obj)

    def store(
        self,
        pdf_paths: List[str],
        term_ranking: DomainTermRanking,
        config: MethodLayerConfig,
    ) -> None:
        dir_name = create_dir_name_from_config(config, prefix="rank")
        file_name = create_file_name_from_paths(pdf_paths, "json")
        cache_file_path = os.path.join(self._cache_dir, dir_name, file_name)

        os.makedirs(os.path.dirname(cache_file_path), exist_ok=True)

        with open(cache_file_path, "w") as json_file:
            json.dump(term_ranking.to_json(), json_file, ensure_ascii=False, indent=2)

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
    # public
    def __init__(self, cache_dir: str):
        super().__init__(cache_dir)
        self._cache_dir = cache_dir

    def load(
        self,
        pdf_paths: List[str],
        config: MethodLayerConfig,
        from_json: Callable[[Dict[str, Any]], RankingData],
    ) -> Union[RankingData, None]:
        dir_name = create_dir_name_from_config(config, prefix="data")
        file_name = create_file_name_from_paths(pdf_paths, "json")
        cache_file_path = os.path.join(self._cache_dir, dir_name, file_name)

        if not os.path.isfile(cache_file_path):
            return None

        with open(cache_file_path, "r") as json_file:
            obj = json.load(json_file)

        return from_json(obj)

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
            json.dump(ranking_data.to_json(), json_file, ensure_ascii=False, indent=2)

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
