import pytest

from py_slides_term.candidates import CandidateTermExtractor


@pytest.fixture
def extractor() -> CandidateTermExtractor:
    return CandidateTermExtractor()


def test_japanese_compound_noun(extractor: CandidateTermExtractor):
    candidates = extractor.extract_from_text("ソフトウェア開発とは何か？")

    assert len(candidates) == 1

    candidate = candidates[0]
    assert candidate.lang == "ja"
    assert str(candidate) == "ソフトウェア開発"


def test_english_compound_noun(extractor: CandidateTermExtractor):
    candidates = extractor.extract_from_text("What is Software Delelopment?")
    assert len(candidates) == 1

    candidate = candidates[0]
    assert candidate.lang == "en"
    assert str(candidate) == "Software Delelopment"


def test_mixed_compound_noun(extractor: CandidateTermExtractor):
    candidates = extractor.extract_from_text("Hoare Logic（Hoare理論）")

    assert len(candidates) == 2

    candidate = candidates[0]
    assert candidate.lang == "ja"
    assert str(candidate) == "Hoare Logic"

    candidate = candidates[1]
    assert candidate.lang == "ja"
    assert str(candidate) == "Hoare 理論"
