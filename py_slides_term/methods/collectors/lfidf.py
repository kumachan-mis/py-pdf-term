from .base import BaseRankingDataCollector
from ..rankingdata import LFIDFRankingData
from py_slides_term.candidates import DomainCandidateTermList
from py_slides_term.analysis import LinguOccurrenceAnalyzer


class LFIDFRankingDataCollector(BaseRankingDataCollector[LFIDFRankingData]):
    # public
    def __init__(self):
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
