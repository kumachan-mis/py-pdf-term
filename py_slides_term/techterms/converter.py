from .data import DomainTermScoreDict
from py_slides_term.methods.data import DomainTermRanking


class RankingToScoreDictConverter:
    # public
    def __init__(self, acceptance_rate: float = 0.9):
        self._acceptance_rate = acceptance_rate

    def convert(self, domain_term_ranking: DomainTermRanking) -> DomainTermScoreDict:
        threshold_idx = int(self._acceptance_rate * len(domain_term_ranking.ranking))
        threshold = domain_term_ranking.ranking[threshold_idx].score
        term_scores = {
            scored_term.term: scored_term.score
            for scored_term in domain_term_ranking.ranking
            if scored_term.score > threshold
        }
        return DomainTermScoreDict(domain_term_ranking.domain, term_scores)
