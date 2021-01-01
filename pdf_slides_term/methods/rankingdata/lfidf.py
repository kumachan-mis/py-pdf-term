from dataclasses import dataclass
from typing import Dict, Optional

from .base import BaseRankingData
from pdf_slides_term.share.data import LinguSeq


@dataclass(frozen=True)
class LFIDFRankingData(BaseRankingData):
    domain: str
    # unique domain name
    lingu_freq: Dict[LinguSeq, int]
    # brute force counting of linguistic sequence occurrences in the domain
    # count even if the term occurs as a part of a phrase
    doc_freq: Dict[LinguSeq, int]
    # number of documents in the domain that contain the term
    # count even if the term occurs as a part of a phrase
    num_docs: int
    # number of documents in the domain
    term_maxsize: Optional[Dict[str, float]] = None
    # max fontsize of the term in the domain
    # default of this is 1.0
