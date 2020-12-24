from xml.etree import ElementTree
from typing import List

from pdf_slides_term.candidates.filter import CandidateTermFilter
from pdf_slides_term.candidates.data import PageCandidateTermList, CandidateTermList
from pdf_slides_term.mecab.tagger import MeCabTagger
from pdf_slides_term.share.data import TechnicalTerm


class CandidateTermExtractor:
    # public
    def __init__(self):
        self._mecab_tagger = MeCabTagger()
        self._filter = CandidateTermFilter()

    def extract(self, xml_path: str) -> CandidateTermList:
        pages = []
        xml_root = ElementTree.parse(xml_path).getroot()
        for page_node in xml_root.iter("page"):
            page_num = int(page_node.get("id"))
            candicate_terms = self._extract_from_page(page_node)
            pages.append(PageCandidateTermList(page_num, candicate_terms))

        return CandidateTermList(xml_path, pages)

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
                    candicate_terms.append(candidate_term)
                candicate_term_morphemes = []

            candidate_term = TechnicalTerm(candicate_term_morphemes, fontsize)
            if self._filter.is_candidate_term(candidate_term):
                candicate_terms.append(candidate_term)
            candicate_term_morphemes = []

        return candicate_terms
