from typing import Type

from ..base import BaseMapper
from ..consts import PACKAGE_NAME
from py_slides_term.candidates import (
    BaseAugmenter,
    JapaneseModifyingParticleAugmenter,
    EnglishAdpositionAugmenter,
)


class AugmenterMapper(BaseMapper[Type[BaseAugmenter]]):
    @classmethod
    def default_mapper(cls):
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