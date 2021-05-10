from .data import DomainTechnicalTermList, PDFTechnicalTermList
from .converter import RankingToScoreDictConverter
from .selector import TechnicalTermSelector
from py_slides_term.candidates import DomainCandidateTermList, PDFCandidateTermList
from py_slides_term.methods import DomainTermRanking


class TechnicalTermExtractor:
    # public
    def __init__(self, max_num_pageterms: int = 14, acceptance_rate: float = 0.75):
        self._converter = RankingToScoreDictConverter(acceptance_rate=acceptance_rate)
        self._selector = TechnicalTermSelector(max_num_pageterms=max_num_pageterms)

    def extract_from_domain(
        self,
        domain_candidates: DomainCandidateTermList,
        domain_term_ranking: DomainTermRanking,
    ) -> DomainTechnicalTermList:
        domain_term_scores = self._converter.convert(domain_term_ranking)
        terms = self._selector.select_from_domain(domain_candidates, domain_term_scores)
        return terms

    def extract_from_pdf(
        self,
        pdf_candidates: PDFCandidateTermList,
        domain_term_ranking: DomainTermRanking,
    ) -> PDFTechnicalTermList:
        domain_term_scores = self._converter.convert(domain_term_ranking)
        terms = self._selector.select_from_pdf(pdf_candidates, domain_term_scores)
        return terms
