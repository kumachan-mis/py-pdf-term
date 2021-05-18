from ..base import BaseJapaneseCandidateTermFilter
from py_slides_term.tokenizer import BaseMorpheme, JapaneseMorphemeClassifier
from py_slides_term.share.data import Term


class JapaneseNumericFilter(BaseJapaneseCandidateTermFilter):
    # public
    def __init__(self):
        self._classifier = JapaneseMorphemeClassifier()

    def is_candidate(self, scoped_term: Term) -> bool:
        is_numeric_phrase = self._is_numeric_phrase(scoped_term)
        has_quantity_phrase = self._has_quantity_phrase(scoped_term)
        return not is_numeric_phrase and not has_quantity_phrase

    def _is_numeric_phrase(self, scoped_term: Term) -> bool:
        def is_number_or_counter_or_meaningless(morpheme: BaseMorpheme) -> bool:
            return (
                (morpheme.pos == "名詞" and morpheme.category == "数詞")
                or (
                    morpheme.pos == "名詞"
                    and morpheme.category == "普通名詞"
                    and morpheme.subcategory == "助数詞可能"
                )
                or self._classifier.is_meaningless(morpheme)
            )

        return all(map(is_number_or_counter_or_meaningless, scoped_term.morphemes))

    def _has_quantity_phrase(self, scoped_term: Term) -> bool:
        num_morphemes = len(scoped_term.morphemes)

        def quantity_phrase_appears_at(i: int) -> bool:
            if i == num_morphemes - 1:
                return False

            morpheme = scoped_term.morphemes[i]
            next_morpheme = scoped_term.morphemes[i + 1]
            return (morpheme.pos == "名詞" and morpheme.category == "数詞") and (
                next_morpheme.pos == "名詞"
                and next_morpheme.category == "普通名詞"
                and next_morpheme.subcategory == "助数詞可能"
            )

        return any(map(quantity_phrase_appears_at, range(num_morphemes)))
