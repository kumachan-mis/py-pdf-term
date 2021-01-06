from xml.etree.ElementTree import parse, Element
from typing import List, Optional, cast

from .filters import (
    CandidateFilter,
    BaseCandidateMorphemeFilter,
    JapaneseMorphemeFilter,
    EnglishMorphemeFilter,
    BaseCandidateTermFilter,
    ConcatenationFilter,
    SymbolLikeFilter,
    ProperNounFilter,
)
from .data import DomainCandidateTermList, PDFCandidateTermList, PageCandidateTermList
from py_slides_term.pdftoxml import PDFnXMLPath, PDFnXMLElement
from py_slides_term.mecab import (
    MeCabTagger,
    MeCabMorphemeClassifier,
    BaseMeCabMorpheme,
)
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
                ConcatenationFilter(),
                SymbolLikeFilter(),
                ProperNounFilter(),
            ]

        self._mecab_tagger = MeCabTagger()
        self._filter = CandidateFilter(morpheme_filters, term_filters)
        self._classifier = MeCabMorphemeClassifier()
        self.modifying_particle_augmentation = modifying_particle_augmentation

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
            candicate_term_morphemes: List[BaseMeCabMorpheme] = []

            morphemes_from_text = self._mecab_tagger.parse(cast(str, text_node.text))
            fontsize = float(cast(str, text_node.get("size")))
            for idx, morpheme in enumerate(morphemes_from_text):
                if self._filter.is_partof_candidate(morphemes_from_text, idx):
                    candicate_term_morphemes.append(morpheme)
                    continue

                candidate_term = Term(candicate_term_morphemes, fontsize)
                if self._filter.is_candidate(candidate_term):
                    augmented_terms = self._augment_term_if_enabled(candidate_term)
                    candicate_terms.extend(augmented_terms)
                    candicate_terms.append(candidate_term)
                candicate_term_morphemes = []

            candidate_term = Term(candicate_term_morphemes, fontsize)
            if self._filter.is_candidate(candidate_term):
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
                if self._classifier.is_modifying_particle(term.morphemes[opsition])
            ]
            + [num_morphemes]
        )
        num_positions = len(modifying_particle_positions)

        augmented_terms = []
        for length in range(1, num_positions - 1):
            for idx in range(num_positions - length):
                i = modifying_particle_positions[idx]
                j = modifying_particle_positions[idx + length]
                morphemes = term.morphemes[i + 1 : j]
                augmented_term = Term(morphemes, term.fontsize, True)
                if self._filter.is_candidate(augmented_term):
                    augmented_terms.append(augmented_term)

        return augmented_terms
