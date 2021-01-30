from xml.etree.ElementTree import parse, Element
from typing import List, Optional, Type, cast

from .filters import (
    FilterCombiner,
    BaseCandidateMorphemeFilter,
    BaseCandidateTermFilter,
)
from .splitters import SplitterCombiner, BaseSplitter
from .augmenters import AugmenterCombiner, BaseAugmenter
from .data import DomainCandidateTermList, PDFCandidateTermList, PageCandidateTermList
from py_slides_term.pdftoxml import PDFnXMLPath, PDFnXMLElement
from py_slides_term.morphemes import SpaCyTokenizer, BaseMorpheme
from py_slides_term.share.data import Term


class CandidateTermExtractor:
    # public
    def __init__(
        self,
        morpheme_filter_clses: Optional[List[Type[BaseCandidateMorphemeFilter]]] = None,
        term_filter_clses: Optional[List[Type[BaseCandidateTermFilter]]] = None,
        splitter_clses: Optional[List[Type[BaseSplitter]]] = None,
        augmenter_clses: Optional[List[Type[BaseAugmenter]]] = None,
    ):
        self._tokenizer = SpaCyTokenizer()

        morpheme_filters = (
            list(map(lambda cls: cls(), morpheme_filter_clses))
            if morpheme_filter_clses is not None
            else None
        )
        term_filters = (
            list(map(lambda cls: cls(), term_filter_clses))
            if term_filter_clses is not None
            else None
        )
        self._filter = FilterCombiner(morpheme_filters, term_filters)

        splitters = (
            list(map(lambda cls: cls(self._filter), splitter_clses))
            if splitter_clses is not None
            else None
        )
        self._splitter = SplitterCombiner(splitters, self._filter)

        augmenters = (
            list(map(lambda cls: cls(self._filter), augmenter_clses))
            if augmenter_clses is not None
            else None
        )
        self._augmenter = AugmenterCombiner(augmenters, self._filter)

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
            candicate_morphemes: List[BaseMorpheme] = []

            morphemes_from_text = self._tokenizer.tokenize(cast(str, text_node.text))
            fontsize = float(cast(str, text_node.get("size")))
            for idx, morpheme in enumerate(morphemes_from_text):
                if self._filter.is_partof_candidate(morphemes_from_text, idx):
                    candicate_morphemes.append(morpheme)
                    continue

                self._update_candicates(candicate_terms, candicate_morphemes, fontsize)
                candicate_morphemes = []

            self._update_candicates(candicate_terms, candicate_morphemes, fontsize)
            candicate_morphemes = []

        return PageCandidateTermList(page_num, candicate_terms)

    def _update_candicates(
        self, candicates: List[Term], morphemes: List[BaseMorpheme], fontsize: float
    ):
        candidate = Term(morphemes, fontsize)
        if not self._filter.is_candidate(candidate):
            return

        splitted_candidates = self._splitter.split(candidate)
        for splitted_candidate in splitted_candidates:
            augmented_candidates = self._augmenter.augment(splitted_candidate)
            candicates.extend(augmented_candidates)
            candicates.append(splitted_candidate)
