from .base import BaseRankingDataCollector
from ..rankingdata import TFIDFRankingData
from py_slides_term.candidates import DomainCandidateTermList
from py_slides_term.analysis import TermOccurrenceAnalyzer, TermMaxsizeAnalyzer


class TFIDFRankingDataCollector(BaseRankingDataCollector[TFIDFRankingData]):
    # public
    def __init__(self, collect_charfont: bool = True):
        super().__init__()

        self._collect_charfont = collect_charfont

        self._termocc_analyzer = TermOccurrenceAnalyzer()
        self._maxsize_analyzer = TermMaxsizeAnalyzer()

    def collect(self, domain_candidates: DomainCandidateTermList) -> TFIDFRankingData:
        termocc = self._termocc_analyzer.analyze(domain_candidates)
        num_docs = len(domain_candidates.pdfs)
        maxsize = (
            self._maxsize_analyzer.analyze(domain_candidates)
            if self._collect_charfont
            else None
        )
        return TFIDFRankingData(
            domain_candidates.domain,
            termocc.term_freq,
            termocc.doc_term_freq,
            num_docs,
            maxsize.term_maxsize if maxsize is not None else None,
        )
