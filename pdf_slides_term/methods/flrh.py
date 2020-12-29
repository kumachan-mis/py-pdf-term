from pdf_slides_term.methods.base import BaseSingleDomainTermRankingMethod
from pdf_slides_term.methods.data import DomainTermRanking
from pdf_slides_term.methods.analyzers.occurrence import TermOccurrenceAnalyzer
from pdf_slides_term.methods.analyzers.concatenation import TermConcatenationAnalyzer
from pdf_slides_term.methods.analyzers.charfont import TermCharFontAnalyzer
from pdf_slides_term.methods.rankers.flrh import FLRHRanker, FLRHRakingData
from pdf_slides_term.candidates.data import DomainCandidateTermList


class FLRHMethod(BaseSingleDomainTermRankingMethod):
    # public
    def __init__(self, consider_charfont: bool = True):
        super().__init__()

        self._consider_charfont = consider_charfont

        self._occurrence_analyzer = TermOccurrenceAnalyzer()
        self._concat_analyzer = TermConcatenationAnalyzer()
        self._char_font_analyzer = TermCharFontAnalyzer()
        self._ranker = FLRHRanker()

    def rank_terms(
        self, domain_candidates: DomainCandidateTermList
    ) -> DomainTermRanking:
        term_freq = self._occurrence_analyzer.analyze_term_freq(domain_candidates)
        term_concat = self._concat_analyzer.analyze(domain_candidates)
        term_maxsize = (
            self._char_font_analyzer.analyze_term_maxsize(domain_candidates)
            if self._consider_charfont
            else None
        )

        ranking_data = FLRHRakingData(
            term_freq, term_concat.left_freq, term_concat.right_freq, term_maxsize
        )
        domain_term_ranking = self._ranker.rank_terms(domain_candidates, ranking_data)
        return domain_term_ranking
