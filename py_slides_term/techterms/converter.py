from .data import MethodTermScoreDict
from py_slides_term.methods import MethodTermRanking


class RankingToScoreDictConverter:
    # public
    def __init__(self, acceptance_rate: float = 0.75):
        self._acceptance_rate = acceptance_rate

    def convert(self, term_ranking: MethodTermRanking) -> MethodTermScoreDict:
        threshold_idx = int(self._acceptance_rate * len(term_ranking.ranking))
        threshold = term_ranking.ranking[threshold_idx].score
        term_scores = {
            scored_term.term: scored_term.score
            for scored_term in term_ranking.ranking
            if scored_term.score > threshold
        }
        return MethodTermScoreDict(term_ranking.domain, term_scores)
