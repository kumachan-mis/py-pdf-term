from .base import BaseRankingDataCollector
from ..rankingdata import MCValueRankingData
from pdf_slides_term.candidates import DomainCandidateTermList
from pdf_slides_term.analysis import (
    TermOccurrenceAnalyzer,
    TermCooccurrenceAnalyzer,
    TermCharFontAnalyzer,
)


class MCValueRankingDataCollector(BaseRankingDataCollector[MCValueRankingData]):
    # public
    def __init__(self, collect_charfont: bool = True):
        super().__init__()

        self._collect_charfont = collect_charfont

        self._occurrence_analyzer = TermOccurrenceAnalyzer()
        self._cooccurrence_analyzer = TermCooccurrenceAnalyzer()
        self._char_font_analyzer = TermCharFontAnalyzer()

    def collect(self, domain_candidates: DomainCandidateTermList) -> MCValueRankingData:
        term_freq = self._occurrence_analyzer.analyze_term_freq(domain_candidates)
        container_terms = self._cooccurrence_analyzer.analyze_container_terms(
            domain_candidates
        )
        term_maxsize = (
            self._char_font_analyzer.analyze_term_maxsize(domain_candidates)
            if self._collect_charfont
            else None
        )
        return MCValueRankingData(
            domain_candidates.domain, term_freq, container_terms, term_maxsize
        )
