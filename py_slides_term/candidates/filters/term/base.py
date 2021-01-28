from abc import ABCMeta, abstractmethod
from py_slides_term.share.data import Term


class BaseCandidateTermFilter(metaclass=ABCMeta):
    # public
    def __init__(self):
        pass

    @abstractmethod
    def inscope(self, term: Term) -> bool:
        raise NotImplementedError(f"{self.__class__.__name__}.within_scope()")

    @abstractmethod
    def is_candidate(self, scoped_term: Term) -> bool:
        raise NotImplementedError(f"{self.__class__.__name__}.is_part_of_candidate()")
