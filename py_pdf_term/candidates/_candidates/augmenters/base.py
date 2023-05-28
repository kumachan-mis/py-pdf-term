from abc import ABCMeta, abstractmethod

from py_pdf_term.tokenizers import Term


class BaseAugmenter(metaclass=ABCMeta):
    """Base class for augmenters of a candidate term.

    When a long term is a candidate, subterms of the long term may be also candidates.
    For example, if "semantic analysis of programming language" is a candidate,
    "semantic analysis" and "programming language" may be also candidates.

    This class is used to augment a candidate term to its subterms.
    """

    def __init__(self) -> None:
        pass

    @abstractmethod
    def augment(self, term: Term) -> list[Term]:
        """Augment a candidate term.

        Args
        ----
            term:
                Candidate term to be augmented.

        Returns
        -------
            list[Term]:
                List of augmented terms. The first term is the original term.
        """

        raise NotImplementedError(f"{self.__class__.__name__}.augment()")
