from dataclasses import dataclass
from typing import Optional, Dict

from pdf_slides_term.methods.rankingdata.base import BaseRankingData


@dataclass(frozen=True)
class TFIDFRankingData(BaseRankingData):
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
    # default of this is 1.0
