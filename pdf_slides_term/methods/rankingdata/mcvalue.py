from dataclasses import dataclass
from typing import Dict, Optional

from pdf_slides_term.methods.rankingdata.base import BaseRankingData


@dataclass(frozen=True)
class MCValueRakingData(BaseRankingData):
    domain: str
    # unique domain name
    term_freq: Dict[str, int]
    # brute force counting of term occurrences in the domain
    # count even if the term occurs as a part of a phrase
    container_freqs: Dict[str, Dict[str, int]]
    # brute force counting of occurrences of (term, container) in the domain
    # (term, container) is valid iff the container contains the term as a subsequence
    term_maxsize: Optional[Dict[str, float]] = None
    # max fontsize of the term in the domain
    # default of this is 1.0
