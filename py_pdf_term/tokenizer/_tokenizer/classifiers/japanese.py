from ..data import Morpheme


class JapaneseMorphemeClassifier:
    def is_modifying_particle(self, morpheme: Morpheme) -> bool:
        return morpheme.surface_form == "の" and morpheme.pos == "助詞"

    def is_symbol(self, morpheme: Morpheme) -> bool:
        return morpheme.pos in {"補助記号"}

    def is_connector_symbol(self, morpheme: Morpheme) -> bool:
        return morpheme.surface_form in {"・", "-"} and morpheme.pos == "補助記号"

    def is_meaningless(self, morpheme: Morpheme) -> bool:
        return self.is_symbol(morpheme) or self.is_modifying_particle(morpheme)
