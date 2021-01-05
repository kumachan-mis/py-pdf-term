from .base import BaseRankingDataCollector
from ..rankingdata import MCValueRankingData
from py_slides_term.candidates import DomainCandidateTermList
from py_slides_term.analysis import (
    TermOccurrenceAnalyzer,
    ContainerTermsAnalyzer,
    TermMaxsizeAnalyzer,
)


class MCValueRankingDataCollector(BaseRankingDataCollector[MCValueRankingData]):
    # public
    def __init__(self, collect_charfont: bool = True):
        super().__init__()

        self._collect_charfont = collect_charfont

        self._termocc_analyzer = TermOccurrenceAnalyzer()
        self._containers_analyzer = ContainerTermsAnalyzer()
        self._maxsize_analyzer = TermMaxsizeAnalyzer()

    def collect(self, domain_candidates: DomainCandidateTermList) -> MCValueRankingData:
        termocc = self._termocc_analyzer.analyze(domain_candidates)
        container_terms = self._containers_analyzer.analyze(domain_candidates)
        maxsize = (
            self._maxsize_analyzer.analyze(domain_candidates)
            if self._collect_charfont
            else None
        )
        return MCValueRankingData(
            domain_candidates.domain,
            termocc.term_freq,
            container_terms.container_terms,
            maxsize.term_maxsize if maxsize is not None else None,
        )
