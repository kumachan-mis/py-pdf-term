from .base import BaseRankingDataCollector
from ..rankingdata import HITSRankingData
from py_pdf_term.candidates import DomainCandidateTermList
from py_pdf_term.analysis import (
    TermOccurrenceAnalyzer,
    TermLeftRightFrequencyAnalyzer,
)


class HITSRankingDataCollector(BaseRankingDataCollector[HITSRankingData]):
    def __init__(self) -> None:
        super().__init__()
        self._termocc_analyzer = TermOccurrenceAnalyzer()
        self._lrfreq_analyzer = TermLeftRightFrequencyAnalyzer()

    def collect(self, domain_candidates: DomainCandidateTermList) -> HITSRankingData:
        termocc = self._termocc_analyzer.analyze(domain_candidates)
        lrfreq = self._lrfreq_analyzer.analyze(domain_candidates)

        return HITSRankingData(
            domain_candidates.domain,
            termocc.term_freq,
            lrfreq.left_freq,
            lrfreq.right_freq,
        )