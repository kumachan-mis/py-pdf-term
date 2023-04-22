from py_pdf_term.candidates import CandidateTermExtractor


def test_japanese_compound_noun() -> None:
    extractor = CandidateTermExtractor()
    candidates = extractor.extract_from_text("ソフトウェア開発とは何か？")
    assert len(candidates) == 1

    candidate = candidates[0]
    assert candidate.lang == "ja"
    assert str(candidate) == "ソフトウェア開発"


def test_english_compound_noun() -> None:
    extractor = CandidateTermExtractor()
    candidates = extractor.extract_from_text("What is Software Delelopment?")
    assert len(candidates) == 1

    candidate = candidates[0]
    assert candidate.lang == "en"
    assert str(candidate) == "Software Delelopment"


def test_mixed_compound_noun() -> None:
    extractor = CandidateTermExtractor()
    candidates = extractor.extract_from_text("Hoare Logic(Hoare理論)")
    assert len(candidates) == 2

    candidate = candidates[0]
    assert candidate.lang == "ja"
    assert str(candidate) == "Hoare Logic"

    candidate = candidates[1]
    assert candidate.lang == "ja"
    assert str(candidate) == "Hoare理論"


def test_japanese_advective_or_verb() -> None:
    extractor = CandidateTermExtractor()
    candidates = extractor.extract_from_text("通る経路の長さ")
    assert len(candidates) == 3

    candidate = candidates[0]
    assert candidate.lang == "ja"
    assert str(candidate) == "経路"

    candidate = candidates[1]
    token = candidate.tokens[0]
    assert candidate.lang == "ja"
    assert token.pos == "形容詞", "test is broken!"
    assert str(candidate) == "長さ"

    candidate = candidates[2]
    token = candidate.tokens[2]
    assert candidate.lang == "ja"
    assert token.pos == "形容詞", "test is broken!"
    assert str(candidate) == "経路の長さ"


def test_english_advective_or_verb() -> None:
    extractor = CandidateTermExtractor()
    candidates = extractor.extract_from_text("fast feature embedding")
    assert len(candidates) == 1

    candidate = candidates[0]
    assert candidate.lang == "en"
    token = candidate.tokens[0]
    assert token.pos == "ADJ", "test is broken!"
    token = candidate.tokens[2]
    assert token.pos == "VERB" and token.category == "VBG", "test is broken!"
    assert str(candidate) == "fast feature embedding"


def test_japanese_nounal_postfix() -> None:
    extractor = CandidateTermExtractor()
    candidates = extractor.extract_from_text("パイプライン化する")
    assert len(candidates) == 1

    candidate = candidates[0]
    token = candidate.tokens[-1]
    assert candidate.lang == "ja"
    assert token.pos == "接尾辞" and token.category == "名詞的", "test is broken!"
    assert str(candidate) == "パイプライン化"


def test_japanese_adjectival_postfix() -> None:
    extractor = CandidateTermExtractor()
    candidates = extractor.extract_from_text("データ的側面と機能的側面と振舞的側面")
    assert len(candidates) == 3

    candidate = candidates[0]
    token = candidate.tokens[1]
    assert candidate.lang == "ja"
    assert token.pos == "接尾辞" and token.category == "形状詞的", "test is broken!"
    assert str(candidate) == "データ的側面"

    candidate = candidates[1]
    token = candidate.tokens[1]
    assert candidate.lang == "ja"
    assert token.pos == "接尾辞" and token.category == "形状詞的", "test is broken!"
    assert str(candidate) == "機能的側面"

    candidate = candidates[2]
    token = candidate.tokens[1]
    assert candidate.lang == "ja"
    assert token.pos == "接尾辞" and token.category == "形状詞的", "test is broken!"
    assert str(candidate) == "振舞的側面"


def test_japanese_symbol() -> None:
    extractor = CandidateTermExtractor()
    candidates = extractor.extract_from_text("ラムダ計算とラムダ式")
    assert len(candidates) == 2

    candidate = candidates[0]
    token = candidate.tokens[0]
    assert candidate.lang == "ja"
    assert token.pos == "記号", "test is broken!"
    assert str(candidate) == "ラムダ計算"

    candidate = candidates[1]
    token = candidate.tokens[0]
    assert candidate.lang == "ja"
    assert token.pos == "記号", "test is broken!"
    assert str(candidate) == "ラムダ式"
