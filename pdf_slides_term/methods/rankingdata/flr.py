from dataclasses import dataclass
from typing import Optional, Dict

from .base import BaseRankingData


@dataclass(frozen=True)
class FLRRankingData(BaseRankingData):
    domain: str
    # unique domain name
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
    # default of this is 1.0
