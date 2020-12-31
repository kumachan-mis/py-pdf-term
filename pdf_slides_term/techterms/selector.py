from pdf_slides_term.techterms.data import (
    DomainTechnicalTermList,
    XMLTechnicalTermList,
    PageTechnicalTermList,
    DomainTermScoreDict,
)
from pdf_slides_term.candidates.data import (
    DomainCandidateTermList,
    XMLCandidateTermList,
    PageCandidateTermList,
)
from pdf_slides_term.share.utils import remove_duplicated_items


class CandidateSelector:
    # public
    def __init__(self, max_num_pageterms: int = 14):
        self._max_num_pageterms = max_num_pageterms

    def select_from_domain(
        self,
        domain_candidates: DomainCandidateTermList,
        domain_term_scores: DomainTermScoreDict,
    ) -> DomainTechnicalTermList:
        xmls = list(
            map(
                lambda xml: self.select_from_xml(xml, domain_term_scores),
                domain_candidates.xmls,
            )
        )
        return DomainTechnicalTermList(domain_candidates.domain, xmls)

    def select_from_xml(
        self,
        xml_candidates: XMLCandidateTermList,
        domain_term_scores: DomainTermScoreDict,
    ) -> XMLTechnicalTermList:
        pages = list(
            map(
                lambda page: self._select_from_page(page, domain_term_scores),
                xml_candidates.pages,
            )
        )
        return XMLTechnicalTermList(xml_candidates.xml_path, pages)

    # private
    def _select_from_page(
        self,
        page_candidates: PageCandidateTermList,
        domain_term_scores: DomainTermScoreDict,
    ) -> PageTechnicalTermList:
        terms = remove_duplicated_items(
            list(
                filter(
                    lambda candidate: candidate in domain_term_scores.term_scores,
                    map(str, page_candidates.candidates),
                )
            )
        )

        if len(terms) > self._max_num_pageterms:
            scores = list(map(lambda term: domain_term_scores.term_scores[term], terms))
            scores.sort(reverse=True)
            threshold = scores[self._max_num_pageterms]
            terms = list(
                filter(
                    lambda term: domain_term_scores.term_scores[term] > threshold,
                    terms,
                )
            )

        return PageTechnicalTermList(page_candidates.page_num, terms)
