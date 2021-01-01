from xml.etree.ElementTree import parse, ElementTree, Element
from typing import List, cast

from .filter import CandidateTermFilter
from .data import DomainCandidateTermList, XMLCandidateTermList, PageCandidateTermList
from pdf_slides_term.mecab import MeCabTagger, MeCabMorphemeFilter, BaseMeCabMorpheme
from pdf_slides_term.share.data import Term


class CandidateTermExtractor:
    # public
    def __init__(self, modifying_particle_augmentation=False):
        self._mecab_tagger = MeCabTagger()
        self._candidates_filter = CandidateTermFilter()
        self._morpheme_filter = MeCabMorphemeFilter()
        self.modifying_particle_augmentation = modifying_particle_augmentation

    def extract_from_domain_files(
        self, domain: str, xml_paths: List[str]
    ) -> DomainCandidateTermList:
        xmls = list(map(self.extract_from_xml_file, xml_paths))
        return DomainCandidateTermList(domain, xmls)

    def extract_from_xml_file(self, xml_path: str) -> XMLCandidateTermList:
        xml_tree = parse(xml_path)
        xml_candidates = self._extract_from_xmltree(xml_path, xml_tree)
        return xml_candidates

    # private
    def _extract_from_xmltree(
        self, xml_path: str, xml_tree: ElementTree
    ) -> XMLCandidateTermList:
        xml_root = xml_tree.getroot()
        page_candidates: List[PageCandidateTermList] = []
        for page in xml_root.iter("page"):
            page_candidates.append(self._extract_from_page(page))

        return XMLCandidateTermList(xml_path, page_candidates)

    def _extract_from_page(self, page: Element) -> PageCandidateTermList:
        page_num = int(cast(str, page.get("id")))

        candicate_terms: List[Term] = []
        for text_node in page.iter("text"):
            candicate_term_morphemes: List[BaseMeCabMorpheme] = []

            morphemes_from_text = self._mecab_tagger.parse(cast(str, text_node.text))
            fontsize = float(cast(str, text_node.get("size")))
            for morpheme in morphemes_from_text:
                if self._candidates_filter.is_part_of_candidate_term(morpheme):
                    candicate_term_morphemes.append(morpheme)
                    continue

                candidate_term = Term(candicate_term_morphemes, fontsize)
                if self._candidates_filter.is_candidate_term(candidate_term):
                    augmented_terms = self._augment_term_if_enabled(candidate_term)
                    candicate_terms.extend(augmented_terms)
                    candicate_terms.append(candidate_term)
                candicate_term_morphemes = []

            candidate_term = Term(candicate_term_morphemes, fontsize)
            if self._candidates_filter.is_candidate_term(candidate_term):
                augmented_terms = self._augment_term_if_enabled(candidate_term)
                candicate_terms.extend(augmented_terms)
                candicate_terms.append(candidate_term)
            candicate_term_morphemes = []

        return PageCandidateTermList(page_num, candicate_terms)

    def _augment_term_if_enabled(self, term: Term) -> List[Term]:
        if not self.modifying_particle_augmentation:
            return []

        num_morphemes = len(term.morphemes)
        modifying_particle_positions = (
            [-1]
            + [
                opsition
                for opsition in range(num_morphemes)
                if self._morpheme_filter.is_modifying_particle(term.morphemes[opsition])
            ]
            + [num_morphemes]
        )
        num_positions = len(modifying_particle_positions)

        augmented_terms = []
        for length in range(1, num_positions - 1):
            for index in range(num_positions - length):
                i = modifying_particle_positions[index]
                j = modifying_particle_positions[index + length]
                morphemes = term.morphemes[i + 1 : j]
                augmented_term = Term(morphemes, term.fontsize, True)
                if self._candidates_filter.is_candidate_term(augmented_term):
                    augmented_terms.append(augmented_term)

        return augmented_terms
