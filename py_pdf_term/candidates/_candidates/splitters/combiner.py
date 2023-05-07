from typing import List, Optional

from py_pdf_term.tokenizers import Term

from .base import BaseSplitter
from .repeat import RepeatSplitter
from .symname import SymbolNameSplitter


class SplitterCombiner:
    """A combiner of splitters.

    Args
    ----
        splitters:
            A list of splitters to split terms. The splitters are applied in order.
            If None, the default splitters are used. The default splitters are
            SymbolNameSplitter and RepeatSplitter.
    """

    def __init__(self, splitters: Optional[List[BaseSplitter]] = None) -> None:
        if splitters is None:
            splitters = [SymbolNameSplitter(), RepeatSplitter()]

        self._splitters = splitters

    def split(self, term: Term) -> List[Term]:
        """Split a wrongly concatenated term.

        Args
        ----
            term:
                A wrongly concatenated term to be split.

        Returns
        -------
            List[Term]:
                A list of split terms.
        """

        splitted_terms = [term]

        for splitter in self._splitters:
            start: List[Term] = []
            splitted_terms = sum(map(splitter.split, splitted_terms), start)

        return splitted_terms
