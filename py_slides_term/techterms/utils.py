from typing import List, Dict, Optional, TypeVar

from .data import ScoredTerm

__T = TypeVar("__T")


def list_remove_dup(__ls: List[__T]) -> List[__T]:
    return [e for i, e in enumerate(__ls) if i == __ls.index(e)]


def ranking_to_dict(
    ranking: List[ScoredTerm], rate: Optional[float] = None
) -> Dict[str, float]:
    if rate is None:
        return {item.term: item.score for item in ranking}

    threshold = ranking[int(rate * len(ranking))].score
    return {item.term: item.score for item in ranking if item.score > threshold}
