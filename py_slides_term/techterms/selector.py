from .data import (
    DomainTechnicalTermList,
    PDFTechnicalTermList,
    PageTechnicalTermList,
    DomainTermScoreDict,
)
from py_slides_term.candidates import (
    DomainCandidateTermList,
    PDFCandidateTermList,
    PageCandidateTermList,
)
from py_slides_term.share.utils import remove_duplicated_items
from py_slides_term.share.data import ScoredTerm


class TechnicalTermSelector:
    # public
    def __init__(self, max_num_pageterms: int = 14):
        self._max_num_pageterms = max_num_pageterms

    def select_from_domain(
        self,
        domain_candidates: DomainCandidateTermList,
        domain_term_scores: DomainTermScoreDict,
    ) -> DomainTechnicalTermList:
        pdfs = list(
            map(
                lambda pdfs: self.select_from_pdf(pdfs, domain_term_scores),
                domain_candidates.pdfs,
            )
        )
        return DomainTechnicalTermList(domain_candidates.domain, pdfs)

    def select_from_pdf(
        self,
        pdf_candidates: PDFCandidateTermList,
        domain_term_scores: DomainTermScoreDict,
    ) -> PDFTechnicalTermList:
        pages = list(
            map(
                lambda page: self._select_from_page(page, domain_term_scores),
                pdf_candidates.pages,
            )
        )
        return PDFTechnicalTermList(pdf_candidates.pdf_path, pages)

    # private
    def _select_from_page(
        self,
        page_candidates: PageCandidateTermList,
        domain_term_scores: DomainTermScoreDict,
    ) -> PageTechnicalTermList:
        scored_terms = remove_duplicated_items(
            [
                ScoredTerm(candidate_str, domain_term_scores.term_scores[candidate_str])
                for candidate_str in map(str, page_candidates.candidates)
                if candidate_str in domain_term_scores.term_scores
            ]
        )

        if len(scored_terms) > self._max_num_pageterms:
            scores = list(map(lambda scored_term: scored_term.score, scored_terms))
            scores.sort(reverse=True)
            threshold = scores[self._max_num_pageterms]
            scored_terms = list(
                filter(lambda scored_term: scored_term.score > threshold, scored_terms)
            )

        return PageTechnicalTermList(page_candidates.page_num, scored_terms)
