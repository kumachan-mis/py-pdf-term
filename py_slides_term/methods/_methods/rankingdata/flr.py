from dataclasses import dataclass
from typing import Dict

from .base import BaseRankingData


@dataclass(frozen=True)
class FLRRankingData(BaseRankingData):
    domain: str
    # unique domain name
    term_freq: Dict[str, int]
    # brute force counting of lemmatized term occurrences in the domain
    # count even if the lemmatized term occurs as a part of a lemmatized phrase
    left_freq: Dict[str, Dict[str, int]]
    # number of occurrences of lemmatized (left, morpheme) in the domain
    # if morpheme or left is meaningless this is fixed at zero
    right_freq: Dict[str, Dict[str, int]]
    # number of occurrences of lemmatized (morpheme, right) in the domain
    # if morpheme or right is meaningless this is fixed at zero