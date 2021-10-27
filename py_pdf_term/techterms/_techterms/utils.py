from typing import Dict, List, Optional

from .data import ScoredTerm


def ranking_to_dict(
    ranking: List[ScoredTerm], rate: Optional[float] = None
) -> Dict[str, float]:
    if rate is None:
        return {item.term: item.score for item in ranking}

    threshold = ranking[int(rate * len(ranking))].score
    return {item.term: item.score for item in ranking if item.score > threshold}
