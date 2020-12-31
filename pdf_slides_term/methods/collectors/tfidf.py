from dataclasses import dataclass
from typing import Optional, Dict

from pdf_slides_term.methods.collectors.base import BaseRankingDataCollector
from pdf_slides_term.candidates.data import DomainCandidateTermList
from pdf_slides_term.analysis.occurrence import TermOccurrenceAnalyzer
from pdf_slides_term.analysis.charfont import TermCharFontAnalyzer


@dataclass(frozen=True)
class TFIDFRankingData:
    domain: str
    # unique domain name
    term_freq: Dict[str, int]
    # brute force counting of term occurrences in the domain
    # count even if the term occurs as a part of a phrase
    doc_freq: Dict[str, int]
    # number of documents in the domain that contain the term
    # count even if the term occurs as a part of a phrase
    num_docs: int
    # number of documents in the domain
    term_maxsize: Optional[Dict[str, float]] = None
    # max fontsize of the term in the domain
    # default of this is zero


class MDPRankingDataCollector(BaseRankingDataCollector[TFIDFRankingData]):
    def __init__(self, collect_charfont: bool = True):
        super().__init__()

        self._collect_charfont = collect_charfont

        self._occurrence_analyzer = TermOccurrenceAnalyzer()
        self._char_font_analyzer = TermCharFontAnalyzer()

    def collect(self, domain_candidates: DomainCandidateTermList) -> TFIDFRankingData:
        term_freq = self._occurrence_analyzer.analyze_term_freq(domain_candidates)
        doc_freq = self._occurrence_analyzer.analyze_doc_freq(domain_candidates)
        num_docs = len(domain_candidates.xmls)
        term_maxsize = (
            self._char_font_analyzer.analyze_term_maxsize(domain_candidates)
            if self._collect_charfont
            else None
        )
        return TFIDFRankingData(
            domain_candidates.domain, term_freq, doc_freq, num_docs, term_maxsize
        )
