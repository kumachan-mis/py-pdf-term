import re
from xml.etree import ElementTree
from typing import List

from pdf_slides_term.morphemes import BaseMeCabMorpheme
from pdf_slides_term.tagger import MeCabTagger
from pdf_slides_term.terms import PageCandidateTermList, TechnicalTerm
from pdf_slides_term.consts import SYMBOLS


class CandidateTermExtractor:
    # public
    def __init__(self):
        self._mecab_tagger = MeCabTagger()
        self._filter = CandidateTermFilter()

    def extract(self, xml_path: str) -> List[PageCandidateTermList]:
        candidate_term_list = []
        xml_root = ElementTree.parse(xml_path).getroot()
        for page_node in xml_root.iter("page"):
            page_num = int(page_node.get("id"))
            candicate_terms = self._extract_from_page(page_node)
            candidate_term_list.append(PageCandidateTermList(page_num, candicate_terms))

        return candidate_term_list

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


class CandidateTermFilter:
    def is_part_of_candidate_term(self, morpheme: BaseMeCabMorpheme) -> bool:
        if morpheme.pos == "名詞":
            valid_categories = {"一般", "サ変接続", "固有名詞", "形容動詞語幹", "接尾"}
            return (
                morpheme.category in valid_categories
                and morpheme.subcategory not in {"助数詞"}
            )
        elif morpheme.pos == "接頭詞":
            return morpheme.category in {"名詞接続"}
        elif morpheme.pos == "動詞":
            return morpheme.category in {"自立"}
        elif morpheme.pos == "形容詞":
            return morpheme.category in {"自立"}
        else:
            return False

    def is_candidate_term(self, term: TechnicalTerm) -> bool:
        invalid_term_regex = re.compile(rf"[a-z{re.escape(SYMBOLS)}]*|[A-Z]")
        if invalid_term_regex.fullmatch(str(term)) is not None:
            return False

        num_morphemes = len(term.morphemes)
        if num_morphemes == 1:
            morpheme = term.morphemes[0]
            return (
                morpheme.pos == "名詞"
                and morpheme.category in {"一般", "サ変接続", "固有名詞"}
                and morpheme.subcategory not in {"人名", "組織", "地域"}
            )

        for i in range(num_morphemes):
            morpheme = term.morphemes[i]
            if morpheme.pos not in {"動詞", "形容詞"}:
                continue

            next_morpheme = term.morphemes[i + 1] if i + 1 < num_morphemes else None
            is_valid_morpheme = (
                next_morpheme is not None
                and next_morpheme.pos == "名詞"
                and next_morpheme.category in {"接尾"}
                and next_morpheme.subcategory in {"特殊"}
            )

            if not is_valid_morpheme:
                return False

        return True
