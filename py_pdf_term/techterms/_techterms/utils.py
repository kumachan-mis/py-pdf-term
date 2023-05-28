from .data import ScoredTerm


def ranking_to_dict(
    ranking: list[ScoredTerm], rate: float | None = None
) -> dict[str, float]:
    if rate is None:
        return {item.term: item.score for item in ranking}

    ranking_len = len(ranking)
    threshold_index = min(max(0, int(rate * ranking_len)), ranking_len - 1)
    threshold = ranking[threshold_index].score

    return {item.term: item.score for item in ranking if item.score >= threshold}
