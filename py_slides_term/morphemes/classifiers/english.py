from ..data import BaseMorpheme


class EnglishMorphemeClassifier:
    # public
    def is_symbol(self, morpheme: BaseMorpheme) -> bool:
        return morpheme.pos == "SYM"

    def is_connector_symbol(self, morpheme: BaseMorpheme) -> bool:
        return morpheme.surface_form == "-" and morpheme.pos == "SYM"
