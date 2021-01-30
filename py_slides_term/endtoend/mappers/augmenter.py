from typing import Type

from .base import BaseMapper
from py_slides_term.candidates import BaseAugmenter, ModifyingParticleAugmenter


class AugmenterMapper(BaseMapper[Type[BaseAugmenter]]):
    @classmethod
    def default_mapper(cls):
        module_path = "py_slides_term.augmenters"
        default_mapper = cls()

        augmenter_clses = [ModifyingParticleAugmenter]
        for augmenter_cls in augmenter_clses:
            default_mapper.add(f"{module_path}.{augmenter_cls.__name__}", augmenter_cls)

        return default_mapper
