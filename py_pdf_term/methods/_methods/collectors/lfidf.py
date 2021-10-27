from py_pdf_term.analysis import LinguOccurrenceAnalyzer
from py_pdf_term.candidates import DomainCandidateTermList

from ..rankingdata import LFIDFRankingData
from .base import BaseRankingDataCollector


class LFIDFRankingDataCollector(BaseRankingDataCollector[LFIDFRankingData]):
    def __init__(self) -> None:
        super().__init__()
        self._linguocc_analyzer = LinguOccurrenceAnalyzer()

    def collect(self, domain_candidates: DomainCandidateTermList) -> LFIDFRankingData:
        linguocc = self._linguocc_analyzer.analyze(domain_candidates)
        num_docs = len(domain_candidates.pdfs)

        return LFIDFRankingData(
            domain_candidates.domain,
            linguocc.lingu_freq,
            linguocc.doc_lingu_freq,
            num_docs,
        )
