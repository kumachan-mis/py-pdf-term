from dataclasses import dataclass
from typing import List, Optional

from pdf_slides_term.mecab.morphemes import BaseMeCabMorpheme


@dataclass
class TechnicalTerm:
    morphemes: List[BaseMeCabMorpheme]
    font_size: Optional[float]

    def __str__(self) -> str:
        return "".join(map(lambda morpheme: morpheme.surface_form, self.morphemes))

    def to_json(self) -> str:
        return str(self)
