from pdf_slides_term.methods.base import BaseSingleDomainTermRankingMethod
from pdf_slides_term.methods.data import DomainTermRanking
from pdf_slides_term.methods.analyzers.charfont import TermCharFontAnalyzer
from pdf_slides_term.methods.analyzers.occurrence import TermOccurrenceAnalyzer
from pdf_slides_term.methods.analyzers.concatenation import TermConcatenationAnalyzer
from pdf_slides_term.methods.rankers.flr import FLRRanker, FLRRakingData
from pdf_slides_term.candidates.data import DomainCandidateTermList


class FLRMethod(BaseSingleDomainTermRankingMethod):
    # public
    def __init__(self):
        super().__init__()
        self._char_font_analyzer = TermCharFontAnalyzer()
        self._occurrence_analyzer = TermOccurrenceAnalyzer()
        self._concat_analyzer = TermConcatenationAnalyzer()
        self._ranker = FLRRanker()

    def rank_terms(
        self, domain_candidates: DomainCandidateTermList
    ) -> DomainTermRanking:
        term_freq = self._occurrence_analyzer.analyze_term_freq(domain_candidates)
        term_maxsize = self._char_font_analyzer.analyze_term_maxsize(domain_candidates)
        concat = self._concat_analyzer.analyze(domain_candidates)

        domain_term_ranking = self._ranker.rank_terms(
            domain_candidates,
            FLRRakingData(term_freq, term_maxsize, concat.left_freq, concat.right_freq),
        )

        return domain_term_ranking
