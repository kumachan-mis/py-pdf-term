from .base import BaseRankingDataCollector
from ..rankingdata import LFIDFRankingData
from py_slides_term.candidates import DomainCandidateTermList
from py_slides_term.analysis import LinguOccurrenceAnalyzer, TermMaxsizeAnalyzer


class LFIDFRankingDataCollector(BaseRankingDataCollector[LFIDFRankingData]):
    # public
    def __init__(self, collect_charfont: bool = True):
        super().__init__()

        self._collect_charfont = collect_charfont

        self._linguocc_analyzer = LinguOccurrenceAnalyzer()
        self._maxsize_analyzer = TermMaxsizeAnalyzer()

    def collect(self, domain_candidates: DomainCandidateTermList) -> LFIDFRankingData:
        linguocc = self._linguocc_analyzer.analyze(domain_candidates)
        num_docs = len(domain_candidates.pdfs)
        maxsize = (
            self._maxsize_analyzer.analyze(domain_candidates)
            if self._collect_charfont
            else None
        )
        return LFIDFRankingData(
            domain_candidates.domain,
            linguocc.lingu_freq,
            linguocc.doc_lingu_freq,
            num_docs,
            maxsize.term_maxsize if maxsize is not None else None,
        )
