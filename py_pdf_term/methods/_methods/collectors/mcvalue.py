from py_pdf_term.analysis import ContainerTermsAnalyzer, TermOccurrenceAnalyzer
from py_pdf_term.candidates import DomainCandidateTermList

from ..rankingdata import MCValueRankingData
from .base import BaseRankingDataCollector


class MCValueRankingDataCollector(BaseRankingDataCollector[MCValueRankingData]):
    def __init__(self) -> None:
        super().__init__()
        self._termocc_analyzer = TermOccurrenceAnalyzer()
        self._containers_analyzer = ContainerTermsAnalyzer()

    def collect(self, domain_candidates: DomainCandidateTermList) -> MCValueRankingData:
        termocc = self._termocc_analyzer.analyze(domain_candidates)
        container_terms = self._containers_analyzer.analyze(domain_candidates)

        return MCValueRankingData(
            domain_candidates.domain,
            termocc.term_freq,
            container_terms.container_terms,
        )
