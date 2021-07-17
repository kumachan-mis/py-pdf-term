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
from .utils import textnode_text, textnode_fontsize, textnode_ncolor
from py_pdf_term.pdftoxml import PDFnXMLPath, PDFnXMLElement
from py_pdf_term.tokenizer import Tokenizer, Morpheme
from py_pdf_term.tokenizer.langs import BaseLanguageTokenizer
from py_pdf_term._common.data import Term


class CandidateTermExtractor:
    def __init__(
        self,
        lang_tokenizer_clses: Optional[List[Type[BaseLanguageTokenizer]]] = None,
        morpheme_filter_clses: Optional[List[Type[BaseCandidateMorphemeFilter]]] = None,
        term_filter_clses: Optional[List[Type[BaseCandidateTermFilter]]] = None,
        splitter_clses: Optional[List[Type[BaseSplitter]]] = None,
        augmenter_clses: Optional[List[Type[BaseAugmenter]]] = None,
    ) -> None:
        lang_tokenizers = (
            list(map(lambda cls: cls(), lang_tokenizer_clses))
            if lang_tokenizer_clses is not None
            else None
        )
        self._tokenizer = Tokenizer(lang_tokenizers=lang_tokenizers)

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
            list(map(lambda cls: cls(), splitter_clses))
            if splitter_clses is not None
            else None
        )
        self._splitter = SplitterCombiner(splitters)

        augmenters = (
            list(map(lambda cls: cls(), augmenter_clses))
            if augmenter_clses is not None
            else None
        )
        self._augmenter = AugmenterCombiner(augmenters)

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

    def extract_from_text(
        self, text: str, fontsize: float = 0.0, ncolor: str = ""
    ) -> List[Term]:
        morphemes = self._tokenizer.tokenize(text)
        return self._extract_from_morphemes(morphemes, fontsize, ncolor)

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
        for textnode in page.iter("text"):
            text = textnode_text(textnode)
            fontsize = textnode_fontsize(textnode)
            ncolor = textnode_ncolor(textnode)
            morphemes = self._tokenizer.tokenize(text)
            terms = self._extract_from_morphemes(morphemes, fontsize, ncolor)
            candicate_terms.extend(terms)

        return PageCandidateTermList(page_num, candicate_terms)

    def _extract_from_morphemes(
        self, morphemes: List[Morpheme], fontsize: float, ncolor: str
    ) -> List[Term]:
        candicate_terms: List[Term] = []
        candicate_morphemes: List[Morpheme] = []
        for idx, morpheme in enumerate(morphemes):
            if self._filter.is_partof_candidate(morphemes, idx):
                candicate_morphemes.append(morpheme)
                continue

            terms = self._terms_from_morphemes(candicate_morphemes, fontsize, ncolor)
            candicate_terms.extend(terms)
            candicate_morphemes = []

        terms = self._terms_from_morphemes(candicate_morphemes, fontsize, ncolor)
        candicate_terms.extend(terms)

        return candicate_terms

    def _terms_from_morphemes(
        self, candicate_morphemes: List[Morpheme], fontsize: float, ncolor: str
    ) -> List[Term]:
        candidate_term = Term(candicate_morphemes, fontsize, ncolor)

        candicate_terms: List[Term] = []
        splitted_candidates = self._splitter.split(candidate_term)
        for splitted_candidate in splitted_candidates:
            augmented_candidates = self._augmenter.augment(splitted_candidate)
            candicate_terms.extend(augmented_candidates)
            candicate_terms.append(splitted_candidate)

        return list(filter(self._filter.is_candidate, candicate_terms))
