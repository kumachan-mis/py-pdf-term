import pytest

from py_slides_term.candidates import CandidateTermExtractor


@pytest.fixture
def extractor() -> CandidateTermExtractor:
    return CandidateTermExtractor()


def test_japanese_modifying_particle_augmenter(
    extractor: CandidateTermExtractor,
) -> None:
    candidates = extractor.extract_from_text("クイックソートの計算量の最悪ケースを考える")

    assert len(candidates) == 6

    candidate = candidates[0]
    assert candidate.lang == "ja"
    assert str(candidate) == "クイックソート"

    candidate = candidates[1]
    assert candidate.lang == "ja"
    assert str(candidate) == "計算量"

    candidate = candidates[2]
    assert candidate.lang == "ja"
    assert str(candidate) == "最悪ケース"

    candidate = candidates[3]
    assert candidate.lang == "ja"
    assert str(candidate) == "クイックソートの計算量"

    candidate = candidates[4]
    assert candidate.lang == "ja"
    assert str(candidate) == "計算量の最悪ケース"

    candidate = candidates[5]
    assert candidate.lang == "ja"
    assert str(candidate) == "クイックソートの計算量の最悪ケース"


def test_english_adposition_augmenter(extractor: CandidateTermExtractor) -> None:
    candidates = extractor.extract_from_text("Introduction to Information Retrieval")

    assert len(candidates) == 3

    candidate = candidates[0]
    assert candidate.lang == "en"
    assert str(candidate) == "Introduction"

    candidate = candidates[1]
    assert candidate.lang == "en"
    assert str(candidate) == "Information Retrieval"

    candidate = candidates[2]
    assert candidate.lang == "en"
    assert str(candidate) == "Introduction to Information Retrieval"
