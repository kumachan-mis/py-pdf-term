from dataclasses import dataclass
from typing import Optional, Dict

from pdf_slides_term.methods.collectors.base import BaseRankingDataCollector
from pdf_slides_term.candidates.data import DomainCandidateTermList
from pdf_slides_term.analysis.occurrence import TermOccurrenceAnalyzer
from pdf_slides_term.analysis.concatenation import TermConcatenationAnalyzer
from pdf_slides_term.analysis.charfont import TermCharFontAnalyzer


@dataclass(frozen=True)
class HITSRakingData:
    term_freq: Dict[str, int]
    # brute force counting of term occurrences in the domain
    # count even if the term occurs as a part of a phrase
    left_freq: Dict[str, Dict[str, int]]
    # number of occurrences of (left, morpheme) in the domain
    # if morpheme or left is a modifying particle, this is fixed at zero
    right_freq: Dict[str, Dict[str, int]]
    # number of occurrences of (morpheme, right) in the domain
    # if morpheme or right is a modifying particle, this is fixed at zero
    term_maxsize: Optional[Dict[str, float]] = None
    # max fontsize of the term in the domain
    # default of this is zero


class FLRHRankingDataCollector(BaseRankingDataCollector[HITSRakingData]):
    # public
    def __init__(self, collect_charfont: bool = True):
        super().__init__()

        self._collect_charfont = collect_charfont

        self._occurrence_analyzer = TermOccurrenceAnalyzer()
        self._concat_analyzer = TermConcatenationAnalyzer()
        self._char_font_analyzer = TermCharFontAnalyzer()

    def collect(self, domain_candidates: DomainCandidateTermList) -> HITSRakingData:
        term_freq = self._occurrence_analyzer.analyze_term_freq(domain_candidates)
        term_concat = self._concat_analyzer.analyze(domain_candidates)
        term_maxsize = (
            self._char_font_analyzer.analyze_term_maxsize(domain_candidates)
            if self._collect_charfont
            else None
        )
        return HITSRakingData(
            term_freq, term_concat.left_freq, term_concat.right_freq, term_maxsize
        )
