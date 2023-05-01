from typing import Type

from py_pdf_term._common.consts import PACKAGE_NAME
from py_pdf_term.candidates.augmenters import (
    BaseAugmenter,
    EnglishConnectorTermAugmenter,
    JapaneseConnectorTermAugmenter,
)

from ..base import BaseMapper


class AugmenterMapper(BaseMapper[Type[BaseAugmenter]]):
    """A mapper to find augmenter classes."""

    @classmethod
    def default_mapper(cls) -> "AugmenterMapper":
        default_mapper = cls()

        augmenter_clses = [
            JapaneseConnectorTermAugmenter,
            EnglishConnectorTermAugmenter,
        ]
        for augmenter_cls in augmenter_clses:
            default_mapper.add(
                f"{PACKAGE_NAME}.{augmenter_cls.__name__}", augmenter_cls
            )

        return default_mapper
