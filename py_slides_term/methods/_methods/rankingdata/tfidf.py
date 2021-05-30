from dataclasses import dataclass
from typing import Dict

from .base import BaseRankingData


@dataclass(frozen=True)
class TFIDFRankingData(BaseRankingData):
    domain: str
    # unique domain name
    term_freq: Dict[str, int]
    # brute force counting of lemmatized term occurrences in the domain
    # count even if the lemmatized term occurs as a part of a lemmatized phrase
    doc_freq: Dict[str, int]
    # number of documents in the domain that contain the lemmatized term
    # count even if the lemmatized term occurs as a part of a lemmatized phrase
    num_docs: int
    # number of documents in the domain
