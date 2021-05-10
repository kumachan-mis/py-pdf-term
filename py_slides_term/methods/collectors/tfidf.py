from .base import BaseRankingDataCollector
from ..rankingdata import TFIDFRankingData
from py_slides_term.candidates import DomainCandidateTermList
from py_slides_term.analysis import TermOccurrenceAnalyzer


class TFIDFRankingDataCollector(BaseRankingDataCollector[TFIDFRankingData]):
    # public
    def __init__(self):
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
