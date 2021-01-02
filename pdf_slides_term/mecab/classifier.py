from .morphemes import BaseMeCabMorpheme


class MeCabMorphemeClassifier:
    def is_modifying_particle(self, morpheme: BaseMeCabMorpheme) -> bool:
        return morpheme.pos == "助詞" and morpheme.category == "連体化"

    def is_symbol(self, morpheme: BaseMeCabMorpheme) -> bool:
        return morpheme.pos == "記号"
