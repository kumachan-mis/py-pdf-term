from pdf_slides_term.methods.collectors.base import BaseRankingDataCollector
from pdf_slides_term.methods.rankingdata.hits import HITSRakingData
from pdf_slides_term.candidates.data import DomainCandidateTermList
from pdf_slides_term.analysis.occurrence import TermOccurrenceAnalyzer
from pdf_slides_term.analysis.concatenation import TermConcatenationAnalyzer
from pdf_slides_term.analysis.charfont import TermCharFontAnalyzer


class HITSRankingDataCollector(BaseRankingDataCollector[HITSRakingData]):
    # public
    def __init__(self, collect_charfont: bool = True):
        super().__init__()

        self._collect_charfont = collect_charfont

        self._occurrence_analyzer = TermOccurrenceAnalyzer()
        self._concat_analyzer = TermConcatenationAnalyzer()
        self._char_font_analyzer = TermCharFontAnalyzer()

    def collect(self, domain_candidates: DomainCandidateTermList) -> HITSRakingData:
        term_freq = self._occurrence_analyzer.analyze_term_freq(domain_candidates)
        term_concat = self._concat_analyzer.analyze(domain_candidates)
        term_maxsize = (
            self._char_font_analyzer.analyze_term_maxsize(domain_candidates)
            if self._collect_charfont
            else None
        )
        return HITSRakingData(
            domain_candidates.domain,
            term_freq,
            term_concat.left_freq,
            term_concat.right_freq,
            term_maxsize,
        )
