from typing import Dict, List, Optional

from .data import ScoredTerm


def ranking_to_dict(
    ranking: List[ScoredTerm], rate: Optional[float] = None
) -> Dict[str, float]:
    if rate is None:
        return {item.term: item.score for item in ranking}

    if rate < 0.0 or rate > 1.0:
        raise ValueError(f"rate must be between 0.0 and 1.0: {rate}")

    ranking_len = len(ranking)
    threshold_index = min(max(0, int(rate * ranking_len)), ranking_len - 1)
    threshold = ranking[threshold_index].score

    return {item.term: item.score for item in ranking if item.score >= threshold}
