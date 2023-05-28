from py_pdf_term.tokenizers import Term

from .base import BaseSplitter
from .repeat import RepeatSplitter
from .symname import SymbolNameSplitter


class SplitterCombiner:
    """Combiner of splitters.

    Args
    ----
        splitters:
            List of splitters to split terms. The splitters are applied in order.
            If None, the default splitters are used. The default splitters are
            SymbolNameSplitter and RepeatSplitter.
    """

    def __init__(self, splitters: list[BaseSplitter] | None = None) -> None:
        if splitters is None:
            splitters = [SymbolNameSplitter(), RepeatSplitter()]

        self._splitters = splitters

    def split(self, term: Term) -> list[Term]:
        """Split a wrongly concatenated term.

        Args
        ----
            term:
                Wrongly concatenated term to be split.

        Returns
        -------
            list[Term]:
                List of split terms.
        """

        splitted_terms = [term]

        for splitter in self._splitters:
            start: list[Term] = []
            splitted_terms = sum(map(splitter.split, splitted_terms), start)

        return splitted_terms
