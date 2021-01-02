from .base import BaseRankingDataCollector
from ..rankingdata import LFIDFRankingData
from py_slides_term.candidates import DomainCandidateTermList
from py_slides_term.analysis import TermOccurrenceAnalyzer, TermCharFontAnalyzer


class LFIDFRankingDataCollector(BaseRankingDataCollector[LFIDFRankingData]):
    # public
    def __init__(self, collect_charfont: bool = True):
        super().__init__()

        self._collect_charfont = collect_charfont

        self._occurrence_analyzer = TermOccurrenceAnalyzer()
        self._char_font_analyzer = TermCharFontAnalyzer()

    def collect(self, domain_candidates: DomainCandidateTermList) -> LFIDFRankingData:
        lingu_freq = self._occurrence_analyzer.analyze_lingu_freq(domain_candidates)
        doc_freq = self._occurrence_analyzer.analyze_doc_lingu_freq(domain_candidates)
        num_docs = len(domain_candidates.pdfs)
        term_maxsize = (
            self._char_font_analyzer.analyze_term_maxsize(domain_candidates)
            if self._collect_charfont
            else None
        )
        return LFIDFRankingData(
            domain_candidates.domain, lingu_freq, doc_freq, num_docs, term_maxsize
        )
