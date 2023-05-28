from py_pdf_term.tokenizers import Term

from .base import BaseAugmenter
from .separation import EnglishConnectorTermAugmenter, JapaneseConnectorTermAugmenter


class AugmenterCombiner:
    """Combiner of augmenters of a candidate term.

    Args
    ----
        augmenters:
            List of augmenters to be combined. The augmenters are applied in order.
            If None, the default augmenters are used. The default augmenters are
            JapaneseConnectorTermAugmenter and EnglishConnectorTermAugmenter.
    """

    def __init__(self, augmenters: list[BaseAugmenter] | None = None) -> None:
        if augmenters is None:
            augmenters = [
                JapaneseConnectorTermAugmenter(),
                EnglishConnectorTermAugmenter(),
            ]

        self._augmenters = augmenters

    def augment(self, term: Term) -> list[Term]:
        """Augment a candidate term.

        Args
        ----
            term:
                Candidate term to be augmented.

        Returns
        -------
            list[Term]:
                List of augmented terms. The the original term is not included in the
                list.
        """

        augmented_terms = [term]
        for augmenter in self._augmenters:
            start: list[Term] = []
            augmented_terms += sum(map(augmenter.augment, augmented_terms), start)

        return augmented_terms[1:]
