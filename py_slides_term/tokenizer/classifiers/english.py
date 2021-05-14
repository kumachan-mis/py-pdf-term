from ..data import BaseMorpheme


class EnglishMorphemeClassifier:
    # public
    def is_adposition(self, morpheme: BaseMorpheme) -> bool:
        return morpheme.pos == "ADP"

    def is_symbol(self, morpheme: BaseMorpheme) -> bool:
        return morpheme.pos == "SYM"

    def is_connector_symbol(self, morpheme: BaseMorpheme) -> bool:
        return morpheme.surface_form == "-" and morpheme.pos == "SYM"

    def is_meaningless(self, morpheme: BaseMorpheme) -> bool:
        return self.is_symbol(morpheme) or self.is_adposition(morpheme)
