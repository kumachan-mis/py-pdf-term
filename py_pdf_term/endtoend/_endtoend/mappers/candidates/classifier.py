from typing import Type

from py_pdf_term.candidates.classifiers import (
    BaseTokenClassifier,
    EnglishTokenClassifier,
    JapaneseTokenClassifier,
)

from ..base import BaseMapper
from ..consts import PACKAGE_NAME


class TokenClassifilerMapper(BaseMapper[Type[BaseTokenClassifier]]):
    @classmethod
    def default_mapper(cls) -> "TokenClassifilerMapper":
        default_mapper = cls()

        classifier_clses = [
            JapaneseTokenClassifier,
            EnglishTokenClassifier,
        ]
        for classifier_cls in classifier_clses:
            default_mapper.add(
                f"{PACKAGE_NAME}.{classifier_cls.__name__}", classifier_cls
            )

        return default_mapper
