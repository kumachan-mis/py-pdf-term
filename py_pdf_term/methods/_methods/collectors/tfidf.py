from py_pdf_term.analysis import TermOccurrenceAnalyzer
from py_pdf_term.candidates import DomainCandidateTermList

from ..rankingdata import TFIDFRankingData
from .base import BaseRankingDataCollector


class TFIDFRankingDataCollector(BaseRankingDataCollector[TFIDFRankingData]):
    def __init__(self) -> None:
        super().__init__()
        self._termocc_analyzer = TermOccurrenceAnalyzer()

    def collect(self, domain_candidates: DomainCandidateTermList) -> TFIDFRankingData:
        termocc = self._termocc_analyzer.analyze(domain_candidates)
        num_docs = len(domain_candidates.pdfs)

        return TFIDFRankingData(
            domain_candidates.domain,
            termocc.term_freq,
            termocc.doc_term_freq,
            num_docs,
        )
