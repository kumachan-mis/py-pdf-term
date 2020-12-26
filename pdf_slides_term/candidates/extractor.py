from xml.etree import ElementTree
from typing import List

from pdf_slides_term.candidates.filter import CandidateTermFilter
from pdf_slides_term.candidates.data import (
    DomainCandidateTermList,
    XMLCandidateTermList,
    PageCandidateTermList,
)
from pdf_slides_term.mecab.tagger import MeCabTagger
from pdf_slides_term.share.data import TechnicalTerm


class CandidateTermExtractor:
    # public
    def __init__(self, enable_modifying_particle_extension=False):
        self._mecab_tagger = MeCabTagger()
        self._filter = CandidateTermFilter()
        self.enable_modifying_particle_extension = enable_modifying_particle_extension

    def extract_from_domain(
        self, domain: str, xml_paths: List[str]
    ) -> DomainCandidateTermList:
        xmls = list(map(self.extract_from_domain, xml_paths))
        return DomainCandidateTermList(domain, xmls)

    def extract_from_xml(self, xml_path: str) -> XMLCandidateTermList:
        pages = []
        xml_root = ElementTree.parse(xml_path).getroot()
        for page_node in xml_root.iter("page"):
            page_num = int(page_node.get("id"))
            candicate_terms = self._extract_from_page(page_node)
            pages.append(PageCandidateTermList(page_num, candicate_terms))

        return XMLCandidateTermList(xml_path, pages)

    # private
    def _extract_from_page(self, page_node: ElementTree.Element) -> List[TechnicalTerm]:
        candicate_terms = []
        for text_node in page_node.iter("text"):
            candicate_term_morphemes = []

            morphemes_from_text = self._mecab_tagger.parse(text_node.text)
            fontsize = float(text_node.get("size"))
            for morpheme in morphemes_from_text:
                if self._filter.is_part_of_candidate_term(morpheme):
                    candicate_term_morphemes.append(morpheme)
                    continue

                candidate_term = TechnicalTerm(candicate_term_morphemes, fontsize)
                if self._filter.is_candidate_term(candidate_term):
                    extended_terms = self._extend_term_if_enabled(candidate_term)
                    candicate_terms.extend(extended_terms)
                candicate_term_morphemes = []

            candidate_term = TechnicalTerm(candicate_term_morphemes, fontsize)
            if self._filter.is_candidate_term(candidate_term):
                extended_terms = self._extend_term_if_enabled(candidate_term)
                candicate_terms.extend(extended_terms)
            candicate_term_morphemes = []

        return candicate_terms

    def _extend_term_if_enabled(self, term: TechnicalTerm) -> List[TechnicalTerm]:
        if not self.enable_modifying_particle_extension:
            return [term]

        num_morphemes = len(term.morphemes)
        modifying_particle_positions = (
            [-1]
            + [
                opsition
                for opsition in range(num_morphemes)
                if self._filter.is_modifying_particle(term.morphemes[opsition])
            ]
            + [num_morphemes]
        )
        num_positions = len(modifying_particle_positions)

        extended_terms = []
        for length in range(1, num_positions):
            for index in range(num_positions - length):
                i = modifying_particle_positions[index]
                j = modifying_particle_positions[index + length]
                extended_term = TechnicalTerm(term.morphemes[i + 1 : j], term.fontsize)
                if self._filter.is_candidate_term(extended_term):
                    extended_terms.append(extended_term)

        return extended_terms
