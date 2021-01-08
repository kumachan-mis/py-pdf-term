from .data import BaseMorpheme


class MorphemeClassifier:
    def is_modifying_particle(self, morpheme: BaseMorpheme) -> bool:
        return morpheme.pos == "助詞" and morpheme.category == "連体化"

    def is_symbol(self, morpheme: BaseMorpheme) -> bool:
        return morpheme.pos == "記号"
