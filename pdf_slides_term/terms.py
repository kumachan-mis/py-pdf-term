from dataclasses import dataclass
from typing import List, Dict, Optional

from pdf_slides_term.morphemes import BaseMorpheme


@dataclass
class TechnicalTerm:
    morphemes: List[BaseMorpheme]
    font_size: Optional[float]

    def __str__(self) -> str:
        return "".join(map(lambda morpheme: morpheme.surface_form, self.morphemes))

    def to_json(self) -> str:
        return str(self)


@dataclass
class PageCandidateTermList:
    page_num: int
    candicate_terms: List[TechnicalTerm]

    def to_json(self) -> Dict:
        return {
            "page_num": self.page_num,
            "candicate_terms": list(
                map(lambda term: term.to_json(), self.candicate_terms)
            ),
        }
