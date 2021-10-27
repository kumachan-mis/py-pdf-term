from py_pdf_term.analysis import TermOccurrenceAnalyzer
from py_pdf_term.candidates import DomainCandidateTermList

from ..rankingdata import MDPRankingData
from .base import BaseRankingDataCollector


class MDPRankingDataCollector(BaseRankingDataCollector[MDPRankingData]):
    def __init__(self) -> None:
        super().__init__()
        self._termocc_analyzer = TermOccurrenceAnalyzer()

    def collect(self, domain_candidates: DomainCandidateTermList) -> MDPRankingData:
        termocc = self._termocc_analyzer.analyze(domain_candidates)
        return MDPRankingData(domain_candidates.domain, termocc.term_freq)
