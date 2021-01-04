from typing import Callable, Iterable

from .base import BaseMultiDomainRankingMethod
from ..rankingdata import MDPRankingData
from ..collectors import MDPRankingDataCollector
from ..rankers import MDPRanker


class MDPMethod(BaseMultiDomainRankingMethod[MDPRankingData]):
    # public
    def __init__(
        self,
        compile_scores: Callable[[Iterable[float]], float] = min,
        consider_charfont: bool = True,
    ):
        collector = MDPRankingDataCollector(collect_charfont=consider_charfont)
        ranker = MDPRanker(compile_scores=compile_scores)
        super().__init__(collector, ranker)
