import json
import os
from glob import glob
from shutil import rmtree
from typing import Any, Callable

from py_pdf_term.methods import MethodTermRanking
from py_pdf_term.methods._methods.rankingdata import BaseRankingData

from ...configs import BaseMethodLayerConfig
from ..util import create_dir_name_from_config, create_file_name_from_paths
from .base import BaseMethodLayerDataCache, BaseMethodLayerRankingCache


class MethodLayerRankingFileCache(BaseMethodLayerRankingCache):
    """Method layer ranking cache that stores and loads term rankings to/from a file.

    Args
    ----
        cache_dir:
            Directory path to store cache files.
    """

    def __init__(self, cache_dir: str) -> None:
        super().__init__(cache_dir)
        self._cache_dir = cache_dir

    def load(
        self,
        pdf_paths: list[str],
        config: BaseMethodLayerConfig,
    ) -> MethodTermRanking | None:
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
        pdf_paths: list[str],
        term_ranking: MethodTermRanking,
        config: BaseMethodLayerConfig,
    ) -> None:
        dir_name = create_dir_name_from_config(config, prefix="rank")
        file_name = create_file_name_from_paths(pdf_paths, "json")
        cache_file_path = os.path.join(self._cache_dir, dir_name, file_name)

        os.makedirs(os.path.dirname(cache_file_path), exist_ok=True)

        with open(cache_file_path, "w") as json_file:
            json.dump(term_ranking.to_dict(), json_file, ensure_ascii=False)

    def remove(self, pdf_paths: list[str], config: BaseMethodLayerConfig) -> None:
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


class MethodLayerDataFileCache[RankingData: BaseRankingData](
    BaseMethodLayerDataCache[RankingData]
):
    """Method layer data cache that stores and loads metadata to to generate term
    rankings to/from a file.

    Args
    ----
        cache_dir:
            Directory path to store cache files.
    """

    def __init__(self, cache_dir: str) -> None:
        super().__init__(cache_dir)
        self._cache_dir = cache_dir

    def load(
        self,
        pdf_paths: list[str],
        config: BaseMethodLayerConfig,
        from_dict: Callable[[dict[str, Any]], RankingData],
    ) -> RankingData | None:
        dir_name = create_dir_name_from_config(config, prefix="data")
        file_name = create_file_name_from_paths(pdf_paths, "json")
        cache_file_path = os.path.join(self._cache_dir, dir_name, file_name)

        if not os.path.isfile(cache_file_path):
            return None

        with open(cache_file_path, "r") as json_file:
            try:
                obj = json.load(json_file)
            except json.JSONDecodeError:
                return None

        return from_dict(obj)

    def store(
        self,
        pdf_paths: list[str],
        ranking_data: RankingData,
        config: BaseMethodLayerConfig,
    ) -> None:
        dir_name = create_dir_name_from_config(config, prefix="data")
        file_name = create_file_name_from_paths(pdf_paths, "json")
        cache_file_path = os.path.join(self._cache_dir, dir_name, file_name)

        os.makedirs(os.path.dirname(cache_file_path), exist_ok=True)

        with open(cache_file_path, "w") as json_file:
            json.dump(ranking_data.to_dict(), json_file, ensure_ascii=False)

    def remove(self, pdf_paths: list[str], config: BaseMethodLayerConfig) -> None:
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
