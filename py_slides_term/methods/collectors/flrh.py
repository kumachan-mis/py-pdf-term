from .base import BaseRankingDataCollector
from ..rankingdata import FLRHRankingData
from py_slides_term.candidates import DomainCandidateTermList
from py_slides_term.analysis import (
    TermOccurrenceAnalyzer,
    TermLeftRightFrequencyAnalyzer,
)


class FLRHRankingDataCollector(BaseRankingDataCollector[FLRHRankingData]):
    # public
    def __init__(self):
        super().__init__()
        self._termocc_analyzer = TermOccurrenceAnalyzer()
        self._lrfreq_analyzer = TermLeftRightFrequencyAnalyzer()

    def collect(self, domain_candidates: DomainCandidateTermList) -> FLRHRankingData:
        termocc = self._termocc_analyzer.analyze(domain_candidates)
        lrfreq = self._lrfreq_analyzer.analyze(domain_candidates)

        return FLRHRankingData(
            domain_candidates.domain,
            termocc.term_freq,
            lrfreq.left_freq,
            lrfreq.right_freq,
        )
