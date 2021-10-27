from py_pdf_term.analysis import TermLeftRightFrequencyAnalyzer, TermOccurrenceAnalyzer
from py_pdf_term.candidates import DomainCandidateTermList

from ..rankingdata import FLRRankingData
from .base import BaseRankingDataCollector


class FLRRankingDataCollector(BaseRankingDataCollector[FLRRankingData]):
    def __init__(self) -> None:
        super().__init__()
        self._termocc_analyzer = TermOccurrenceAnalyzer()
        self._lrfreq_analyzer = TermLeftRightFrequencyAnalyzer()

    def collect(self, domain_candidates: DomainCandidateTermList) -> FLRRankingData:
        termocc = self._termocc_analyzer.analyze(domain_candidates)
        lrfreq = self._lrfreq_analyzer.analyze(domain_candidates)

        return FLRRankingData(
            domain_candidates.domain,
            termocc.term_freq,
            lrfreq.left_freq,
            lrfreq.right_freq,
        )
