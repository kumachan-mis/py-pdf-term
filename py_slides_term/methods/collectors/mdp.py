from .base import BaseRankingDataCollector
from ..rankingdata import MDPRankingData
from py_slides_term.candidates import DomainCandidateTermList
from py_slides_term.analysis import TermOccurrenceAnalyzer, TermCharFontAnalyzer


class MDPRankingDataCollector(BaseRankingDataCollector[MDPRankingData]):
    # public
    def __init__(self, collect_charfont: bool = True):
        super().__init__()

        self._collect_charfont = collect_charfont

        self._occurrence_analyzer = TermOccurrenceAnalyzer()
        self._char_font_analyzer = TermCharFontAnalyzer()

    def collect(self, domain_candidates: DomainCandidateTermList) -> MDPRankingData:
        term_freq = self._occurrence_analyzer.analyze_term_freq(domain_candidates)
        term_maxsize = (
            self._char_font_analyzer.analyze_term_maxsize(domain_candidates)
            if self._collect_charfont
            else None
        )
        return MDPRankingData(domain_candidates.domain, term_freq, term_maxsize)
