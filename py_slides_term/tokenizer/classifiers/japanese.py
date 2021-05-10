from ..data import BaseMorpheme


class JapaneseMorphemeClassifier:
    # public
    def is_modifying_particle(self, morpheme: BaseMorpheme) -> bool:
        return morpheme.surface_form == "の" and morpheme.pos == "助詞"

    def is_symbol(self, morpheme: BaseMorpheme) -> bool:
        return morpheme.pos in {"記号", "補助記号"}

    def is_connector_symbol(self, morpheme: BaseMorpheme) -> bool:
        return morpheme.surface_form in {"・", "-"} and morpheme.pos == "補助記号"

    def is_meaningless(self, morpheme: BaseMorpheme) -> bool:
        return self.is_symbol(morpheme) or self.is_modifying_particle(morpheme)
