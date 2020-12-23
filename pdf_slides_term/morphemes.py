from abc import ABCMeta
from dataclasses import dataclass
from typing import ClassVar


@dataclass
class BaseMeCabMorpheme(metaclass=ABCMeta):
    NUM_ATTR: ClassVar[int] = 1

    surface_form: str


@dataclass
class MeCabMorphemeIPADic(BaseMeCabMorpheme):
    NUM_ATTR: ClassVar[int] = 10

    surface_form: str
    pos: str
    category: str
    subcategory: str
    subsubcategory: str
    conjugation_type: str
    conjugation_form: str
    original_form: str
    reading: str
    pronunciation: str
