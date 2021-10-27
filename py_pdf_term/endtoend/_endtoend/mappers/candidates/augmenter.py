from typing import Type

from py_pdf_term.candidates.augmenters import (
    BaseAugmenter,
    EnglishAdpositionAugmenter,
    JapaneseModifyingParticleAugmenter,
)

from ..base import BaseMapper
from ..consts import PACKAGE_NAME


class AugmenterMapper(BaseMapper[Type[BaseAugmenter]]):
    @classmethod
    def default_mapper(cls) -> "AugmenterMapper":
        default_mapper = cls()

        augmenter_clses = [
            JapaneseModifyingParticleAugmenter,
            EnglishAdpositionAugmenter,
        ]
        for augmenter_cls in augmenter_clses:
            default_mapper.add(
                f"{PACKAGE_NAME}.{augmenter_cls.__name__}", augmenter_cls
            )

        return default_mapper
