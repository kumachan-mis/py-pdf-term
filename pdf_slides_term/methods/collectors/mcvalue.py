from pdf_slides_term.methods.collectors.base import BaseRankingDataCollector
from pdf_slides_term.methods.rankingdata.mcvalue import MCValueRakingData
from pdf_slides_term.candidates.data import DomainCandidateTermList
from pdf_slides_term.analysis.occurrence import TermOccurrenceAnalyzer
from pdf_slides_term.analysis.cooccurrence import TermCooccurrenceAnalyzer
from pdf_slides_term.analysis.charfont import TermCharFontAnalyzer


class MCValueRankingDataCollector(BaseRankingDataCollector[MCValueRakingData]):
    # public
    def __init__(self, collect_charfont: bool = True):
        super().__init__()

        self._collect_charfont = collect_charfont

        self._occurrence_analyzer = TermOccurrenceAnalyzer()
        self._cooccurrence_analyzer = TermCooccurrenceAnalyzer()
        self._char_font_analyzer = TermCharFontAnalyzer()

    def collect(self, domain_candidates: DomainCandidateTermList) -> MCValueRakingData:
        term_freq = self._occurrence_analyzer.analyze_term_freq(domain_candidates)
        container_freqs = self._cooccurrence_analyzer.analyze_container_freqs(
            domain_candidates
        )
        term_maxsize = (
            self._char_font_analyzer.analyze_term_maxsize(domain_candidates)
            if self._collect_charfont
            else None
        )
        return MCValueRakingData(
            domain_candidates.domain, term_freq, container_freqs, term_maxsize
        )
