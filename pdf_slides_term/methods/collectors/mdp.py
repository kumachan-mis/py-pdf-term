from dataclasses import dataclass, field
from typing import Optional, Dict

from pdf_slides_term.methods.collectors.base import BaseRankingDataCollector
from pdf_slides_term.candidates.data import DomainCandidateTermList
from pdf_slides_term.analysis.occurrence import TermOccurrenceAnalyzer
from pdf_slides_term.analysis.charfont import TermCharFontAnalyzer


@dataclass(frozen=True)
class MDPRankingData:
    domain: str
    # unique domain name
    term_freq: Dict[str, int]
    # brute force counting of term occurrences in the domain
    # count even if the term occurs as a part of a phrase
    num_terms: int = field(init=False)
    # brute force counting of all terms occurrences in the domain
    # count even if the term occurs as a part of a phrase
    term_maxsize: Optional[Dict[str, float]] = None
    # max fontsize of the term in the domain
    # default of this is zero

    def __post_init__(self):
        object.__setattr__(self, "num_terms", sum(self.term_freq.values()))


class MDPRankingDataCollector(BaseRankingDataCollector[MDPRankingData]):
    # public
    def __init__(self, collect_charfont: bool = True):
        super().__init__()

        self._collect_charfont = collect_charfont

        self._occurrence_analyzer = TermOccurrenceAnalyzer()
        self._char_font_analyzer = TermCharFontAnalyzer()

    def collect(self, domain_candidates: DomainCandidateTermList) -> MDPRankingData:
        term_freq = self._occurrence_analyzer.analyze_term_freq(domain_candidates)
        term_maxsize = (
            self._char_font_analyzer.analyze_term_maxsize(domain_candidates)
            if self._collect_charfont
            else None
        )
        return MDPRankingData(domain_candidates.domain, term_freq, term_maxsize)
