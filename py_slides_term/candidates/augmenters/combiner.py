from typing import List, Optional, cast

from .base import BaseAugmenter
from .separation import JapaneseModifyingParticleAugmenter, EnglishAdpositionAugmenter
from ..filters import FilterCombiner
from py_slides_term.share.data import Term


class AugmenterCombiner:
    def __init__(
        self,
        augmenters: Optional[List[BaseAugmenter]] = None,
        candidate_filter: Optional[FilterCombiner] = None,
    ):
        if augmenters is None:
            if candidate_filter is None:
                raise ValueError("both of 'augmenters' and 'candidate_filter' are None")

            augmenters = [
                JapaneseModifyingParticleAugmenter(candidate_filter),
                EnglishAdpositionAugmenter(candidate_filter),
            ]

        self._augmenters = augmenters

    def augment(self, term: Term) -> List[Term]:
        augmented_terms = [term]

        for augmenter in self._augmenters:
            augmented_terms = sum(
                map(augmenter.augment, augmented_terms), cast(List[Term], [])
            )

        return augmented_terms
