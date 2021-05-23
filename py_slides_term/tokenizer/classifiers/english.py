from ..data import Morpheme


class EnglishMorphemeClassifier:
    def is_adposition(self, morpheme: Morpheme) -> bool:
        return morpheme.pos == "ADP"

    def is_symbol(self, morpheme: Morpheme) -> bool:
        return morpheme.pos == "SYM"

    def is_connector_symbol(self, morpheme: Morpheme) -> bool:
        return morpheme.surface_form == "-" and morpheme.pos == "SYM"

    def is_meaningless(self, morpheme: Morpheme) -> bool:
        return self.is_symbol(morpheme) or self.is_adposition(morpheme)
