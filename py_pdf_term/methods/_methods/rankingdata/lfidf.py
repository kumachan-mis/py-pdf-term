from dataclasses import dataclass
from typing import Dict

from py_pdf_term._common.data import LinguSeq

from .base import BaseRankingData


@dataclass(frozen=True)
class LFIDFRankingData(BaseRankingData):
    domain: str
    # unique domain name
    lingu_freq: Dict[LinguSeq, int]
    # brute force counting of linguistic sequence occurrences in the domain
    # count even if the lemmatized term occurs as a part of a lemmatized phrase
    doc_freq: Dict[LinguSeq, int]
    # number of documents in the domain that contain the term
    # count even if the lemmatized term occurs as a part of a lemmatized phrase
    num_docs: int
    # number of documents in the domain
