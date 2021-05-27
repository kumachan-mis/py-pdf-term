import pytest

from py_slides_term.candidates import CandidateTermExtractor


@pytest.fixture
def extractor() -> CandidateTermExtractor:
    return CandidateTermExtractor()


def test_japanese_compound_noun(extractor: CandidateTermExtractor) -> None:
    candidates = extractor.extract_from_text("ソフトウェア開発とは何か？")
    assert len(candidates) == 1

    candidate = candidates[0]
    assert candidate.lang == "ja"
    assert str(candidate) == "ソフトウェア開発"


def test_english_compound_noun(extractor: CandidateTermExtractor) -> None:
    candidates = extractor.extract_from_text("What is Software Delelopment?")
    assert len(candidates) == 1

    candidate = candidates[0]
    assert candidate.lang == "en"
    assert str(candidate) == "Software Delelopment"


def test_mixed_compound_noun(extractor: CandidateTermExtractor) -> None:
    candidates = extractor.extract_from_text("Hoare Logic（Hoare理論）")
    assert len(candidates) == 2

    candidate = candidates[0]
    assert candidate.lang == "ja"
    assert str(candidate) == "Hoare Logic"

    candidate = candidates[1]
    assert candidate.lang == "ja"
    assert str(candidate) == "Hoare理論"


def test_japanese_advective_or_verb(extractor: CandidateTermExtractor) -> None:
    candidates = extractor.extract_from_text("通る経路の長さ")
    assert len(candidates) == 3

    candidate = candidates[0]
    assert candidate.lang == "ja"
    assert str(candidate) == "経路"

    candidate = candidates[1]
    morpheme = candidate.morphemes[0]
    assert candidate.lang == "ja"
    assert morpheme.pos == "形容詞", "test is broken!"
    assert str(candidate) == "長さ"

    candidate = candidates[2]
    morpheme = candidate.morphemes[2]
    assert candidate.lang == "ja"
    assert morpheme.pos == "形容詞", "test is broken!"
    assert str(candidate) == "経路の長さ"


def test_japanese_nounal_postfix(extractor: CandidateTermExtractor) -> None:
    candidates = extractor.extract_from_text("パイプライン化する")
    assert len(candidates) == 1

    candidate = candidates[0]
    morpheme = candidate.morphemes[-1]
    assert candidate.lang == "ja"
    assert morpheme.pos == "接尾辞" and morpheme.category == "名詞的", "test is broken!"
    assert str(candidate) == "パイプライン化"


def test_japanese_adjectival_postfix(extractor: CandidateTermExtractor) -> None:
    candidates = extractor.extract_from_text("データ的側面と機能的側面と振舞的側面")
    assert len(candidates) == 3

    candidate = candidates[0]
    morpheme = candidate.morphemes[1]
    assert candidate.lang == "ja"
    assert morpheme.pos == "接尾辞" and morpheme.category == "形状詞的", "test is broken!"
    assert str(candidate) == "データ的側面"

    candidate = candidates[1]
    morpheme = candidate.morphemes[1]
    assert candidate.lang == "ja"
    assert morpheme.pos == "接尾辞" and morpheme.category == "形状詞的", "test is broken!"
    assert str(candidate) == "機能的側面"

    candidate = candidates[2]
    morpheme = candidate.morphemes[1]
    assert candidate.lang == "ja"
    assert morpheme.pos == "接尾辞" and morpheme.category == "形状詞的", "test is broken!"
    assert str(candidate) == "振舞的側面"


def test_japanese_symbol(extractor: CandidateTermExtractor) -> None:
    candidates = extractor.extract_from_text("ラムダ計算とラムダ式")
    assert len(candidates) == 2

    candidate = candidates[0]
    morpheme = candidate.morphemes[0]
    assert candidate.lang == "ja"
    assert morpheme.pos == "記号", "test is broken!"
    assert str(candidate) == "ラムダ計算"

    candidate = candidates[1]
    morpheme = candidate.morphemes[0]
    assert candidate.lang == "ja"
    assert morpheme.pos == "記号", "test is broken!"
    assert str(candidate) == "ラムダ式"


def test_english_advective_or_verb(extractor: CandidateTermExtractor) -> None:
    candidates = extractor.extract_from_text("unsupervised feature embedding")
    assert len(candidates) == 1

    candidate = candidates[0]
    assert candidate.lang == "en"
    morpheme = candidate.morphemes[0]
    assert morpheme.pos == "ADJ", "test is broken!"
    morpheme = candidate.morphemes[2]
    assert morpheme.pos == "VERB" and morpheme.category == "VBG", "test is broken!"
    assert str(candidate) == "unsupervised feature embedding"
