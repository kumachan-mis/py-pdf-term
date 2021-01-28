from xml.etree.ElementTree import parse, Element
from typing import List, Optional, cast

from .filters import (
    CandidateFilter,
    BaseCandidateMorphemeFilter,
    JapaneseMorphemeFilter,
    EnglishMorphemeFilter,
    BaseCandidateTermFilter,
    JapaneseConcatenationFilter,
    EnglishConcatenationFilter,
    JapaneseSymbolLikeFilter,
    EnglishSymbolLikeFilter,
    JapaneseProperNounFilter,
    EnglishProperNounFilter,
)
from .augmenters import ModifyingParticleAugmenter
from .data import DomainCandidateTermList, PDFCandidateTermList, PageCandidateTermList
from py_slides_term.pdftoxml import PDFnXMLPath, PDFnXMLElement
from py_slides_term.morphemes import SpaCyTokenizer, BaseMorpheme
from py_slides_term.share.data import Term


class CandidateTermExtractor:
    # public
    def __init__(
        self,
        morpheme_filters: Optional[List[BaseCandidateMorphemeFilter]] = None,
        term_filters: Optional[List[BaseCandidateTermFilter]] = None,
        modifying_particle_augmentation: bool = False,
    ):
        if morpheme_filters is None:
            morpheme_filters = [
                JapaneseMorphemeFilter(),
                EnglishMorphemeFilter(),
            ]
        if term_filters is None:
            term_filters = [
                JapaneseConcatenationFilter(),
                EnglishConcatenationFilter(),
                JapaneseSymbolLikeFilter(),
                EnglishSymbolLikeFilter(),
                JapaneseProperNounFilter(),
                EnglishProperNounFilter(),
            ]

        self._tokenizer = SpaCyTokenizer()
        self._filter = CandidateFilter(morpheme_filters, term_filters)
        self._mp_augmenter = (
            ModifyingParticleAugmenter(self._filter)
            if modifying_particle_augmentation
            else None
        )

    def extract_from_domain_files(
        self, domain: str, pdfnxmls: List[PDFnXMLPath]
    ) -> DomainCandidateTermList:
        xmls = list(map(self.extract_from_xml_file, pdfnxmls))
        return DomainCandidateTermList(domain, xmls)

    def extract_from_xml_file(self, pdfnxml: PDFnXMLPath) -> PDFCandidateTermList:
        xml_root = parse(pdfnxml.xml_path).getroot()
        xml_candidates = self._extract_from_xmlroot(pdfnxml.pdf_path, xml_root)
        return xml_candidates

    def extract_from_domain_elements(
        self, domain: str, pdfnxmls: List[PDFnXMLElement]
    ) -> DomainCandidateTermList:
        xmls = list(map(self.extract_from_xml_element, pdfnxmls))
        return DomainCandidateTermList(domain, xmls)

    def extract_from_xml_element(self, pdfnxml: PDFnXMLElement) -> PDFCandidateTermList:
        xml_candidates = self._extract_from_xmlroot(pdfnxml.pdf_path, pdfnxml.xml_root)
        return xml_candidates

    # private
    def _extract_from_xmlroot(
        self, pdf_path: str, xml_root: Element
    ) -> PDFCandidateTermList:
        page_candidates: List[PageCandidateTermList] = []
        for page in xml_root.iter("page"):
            page_candidates.append(self._extract_from_page(page))

        return PDFCandidateTermList(pdf_path, page_candidates)

    def _extract_from_page(self, page: Element) -> PageCandidateTermList:
        page_num = int(cast(str, page.get("id")))

        candicate_terms: List[Term] = []
        for text_node in page.iter("text"):
            candicate_term_morphemes: List[BaseMorpheme] = []

            morphemes_from_text = self._tokenizer.tokenize(cast(str, text_node.text))
            fontsize = float(cast(str, text_node.get("size")))
            for idx, morpheme in enumerate(morphemes_from_text):
                if self._filter.is_partof_candidate(morphemes_from_text, idx):
                    candicate_term_morphemes.append(morpheme)
                    continue

                candidate_term = Term(candicate_term_morphemes, fontsize)
                if self._filter.is_candidate(candidate_term):
                    if self._mp_augmenter:
                        augmented_terms = self._mp_augmenter.augment(candidate_term)
                        candicate_terms.extend(augmented_terms)

                    candicate_terms.append(candidate_term)
                candicate_term_morphemes = []

            candidate_term = Term(candicate_term_morphemes, fontsize)
            if self._filter.is_candidate(candidate_term):
                if self._mp_augmenter:
                    augmented_terms = self._mp_augmenter.augment(candidate_term)
                    candicate_terms.extend(augmented_terms)

                candicate_terms.append(candidate_term)
            candicate_term_morphemes = []

        return PageCandidateTermList(page_num, candicate_terms)
