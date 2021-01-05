from .base import BaseRankingDataCollector
from ..rankingdata import FLRRankingData
from py_slides_term.candidates import DomainCandidateTermList
from py_slides_term.analysis import (
    TermOccurrenceAnalyzer,
    TermLeftRightFrequencyAnalyzer,
    TermMaxsizeAnalyzer,
)


class FLRRankingDataCollector(BaseRankingDataCollector[FLRRankingData]):
    # public
    def __init__(self, collect_charfont: bool = True):
        super().__init__()

        self._collect_charfont = collect_charfont

        self._termocc_analyzer = TermOccurrenceAnalyzer()
        self._lrfreq_analyzer = TermLeftRightFrequencyAnalyzer()
        self._maxsize_analyzer = TermMaxsizeAnalyzer()

    def collect(self, domain_candidates: DomainCandidateTermList) -> FLRRankingData:
        termocc = self._termocc_analyzer.analyze(domain_candidates)
        lrfreq = self._lrfreq_analyzer.analyze(domain_candidates)
        maxsize = (
            self._maxsize_analyzer.analyze(domain_candidates)
            if self._collect_charfont
            else None
        )
        return FLRRankingData(
            domain_candidates.domain,
            termocc.term_freq,
            lrfreq.left_freq,
            lrfreq.right_freq,
            maxsize.term_maxsize if maxsize is not None else None,
        )
