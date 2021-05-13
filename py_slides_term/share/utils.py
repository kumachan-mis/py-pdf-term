from math import log, log2, log10
from typing import List, Dict, Optional, SupportsFloat, TypeVar

from .data import ScoredTerm

__T = TypeVar("__T")


def extended_log(x: SupportsFloat, base: SupportsFloat) -> float:
    float_x = float(x)
    if float_x > 0.0:
        return log(float_x + 1.0, base)
    if float_x < 0.0:
        return -log(-float_x + 1.0, base)
    else:
        return 0.0


def extended_log2(__x: SupportsFloat) -> float:
    float_x = float(__x)
    if float_x > 0.0:
        return log2(float_x + 1.0)
    if float_x < 0.0:
        return -log2(-float_x + 1.0)
    else:
        return 0.0


def extended_log10(__x: SupportsFloat) -> float:
    float_x = float(__x)
    if float_x > 0.0:
        return log10(float_x + 1.0)
    if float_x < 0.0:
        return -log10(-float_x + 1.0)
    else:
        return 0.0


def list_remove_dup(__ls: List[__T]) -> List[__T]:
    return [e for i, e in enumerate(__ls) if i == __ls.index(e)]


def ranking_to_dict(
    ranking: List[ScoredTerm], rate: Optional[float] = None
) -> Dict[str, float]:
    if rate is None:
        return {scored_term.term: scored_term.score for scored_term in ranking}

    threshold = ranking[int(rate * len(ranking))].score
    term_scores = {
        scored_term.term: scored_term.score
        for scored_term in ranking
        if scored_term.score > threshold
    }
    return term_scores
