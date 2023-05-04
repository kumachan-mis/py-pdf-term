from typing import Type

from py_pdf_term._common.consts import PACKAGE_NAME
from py_pdf_term.candidates.classifiers import (
    BaseTokenClassifier,
    EnglishTokenClassifier,
    JapaneseTokenClassifier,
)

from ..base import BaseMapper


class TokenClassifierMapper(BaseMapper[Type[BaseTokenClassifier]]):
    """A mapper to find token classifier classes."""

    @classmethod
    def default_mapper(cls) -> "TokenClassifierMapper":
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
