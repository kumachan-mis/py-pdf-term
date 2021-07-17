from py_pdf_term.candidates import CandidateTermExtractor


def test_meaningful_space() -> None:
    extractor = CandidateTermExtractor()
    candidates = extractor.extract_from_text("プログラミング言語 型体系")
    assert len(candidates) == 2

    candidate = candidates[0]
    assert candidate.lang == "ja"
    assert str(candidate) == "プログラミング言語"

    candidate = candidates[1]
    assert candidate.lang == "ja"
    assert str(candidate) == "型体系"


def test_meaningless_space() -> None:
    extractor = CandidateTermExtractor()
    candidates = extractor.extract_from_text("情報通信ネットワ ーク")
    assert len(candidates) == 1

    candidate = candidates[0]
    assert candidate.lang == "ja"
    assert str(candidate) == "情報通信ネットワーク"


def test_meaningful_space_with_space_post_english() -> None:
    extractor = CandidateTermExtractor()
    candidates = extractor.extract_from_text("型体系 プログラミング言語 Programming Language")
    assert len(candidates) == 2

    candidate = candidates[0]
    assert candidate.lang == "ja"
    assert str(candidate) == "型体系"

    candidate = candidates[1]
    assert candidate.lang == "ja"
    assert str(candidate) == "プログラミング言語Programming Language"


def test_meaningful_space_with_nospace_post_english() -> None:
    extractor = CandidateTermExtractor()
    candidates = extractor.extract_from_text("型体系 プログラミング言語Programming Language")
    assert len(candidates) == 2

    candidate = candidates[0]
    assert candidate.lang == "ja"
    assert str(candidate) == "型体系"

    candidate = candidates[1]
    assert candidate.lang == "ja"
    assert str(candidate) == "プログラミング言語Programming Language"


def test_meaningful_space_with_space_pre_english() -> None:
    extractor = CandidateTermExtractor()
    candidates = extractor.extract_from_text("Programming Language プログラミング言語 型体系")
    assert len(candidates) == 2

    candidate = candidates[0]
    assert candidate.lang == "ja"
    assert str(candidate) == "Programming Languageプログラミング言語"

    candidate = candidates[1]
    assert candidate.lang == "ja"
    assert str(candidate) == "型体系"


def test_meaningful_space_with_nospace_pre_english() -> None:
    extractor = CandidateTermExtractor()
    candidates = extractor.extract_from_text("Programming Languageプログラミング言語 型体系")
    assert len(candidates) == 2

    candidate = candidates[0]
    assert candidate.lang == "ja"
    assert str(candidate) == "Programming Languageプログラミング言語"

    candidate = candidates[1]
    assert candidate.lang == "ja"
    assert str(candidate) == "型体系"


def test_meaningless_space_with_space_post_english() -> None:
    extractor = CandidateTermExtractor()
    candidates = extractor.extract_from_text("情報通信ネ ットワー ク OSI reference model")
    assert len(candidates) == 1

    candidate = candidates[0]
    assert candidate.lang == "ja"
    assert str(candidate) == "情報通信ネットワークOSI reference model"


def test_meaningless_space_with_nospace_post_english() -> None:
    extractor = CandidateTermExtractor()
    candidates = extractor.extract_from_text("情報通信ネ ットワー クOSI reference model")
    assert len(candidates) == 1

    candidate = candidates[0]
    assert candidate.lang == "ja"
    assert str(candidate) == "情報通信ネットワークOSI reference model"


def test_meaningless_space_with_space_pre_english() -> None:
    extractor = CandidateTermExtractor()
    candidates = extractor.extract_from_text("computer network 情報通信ネ ットワー ク")

    assert len(candidates) == 1

    candidate = candidates[0]
    assert candidate.lang == "ja"
    assert str(candidate) == "computer network情報通信ネットワーク"


def test_meaningless_space_with_nospace_pre_english() -> None:
    extractor = CandidateTermExtractor()
    candidates = extractor.extract_from_text("computer network情報通信ネ ットワー ク")

    assert len(candidates) == 1

    candidate = candidates[0]
    assert candidate.lang == "ja"
    assert str(candidate) == "computer network情報通信ネットワーク"


def test_meaningful_spaces_both_sides_of_english() -> None:
    extractor = CandidateTermExtractor()
    candidates = extractor.extract_from_text("分散 分析 ANOVA が 使える")

    assert len(candidates) == 2

    candidate = candidates[0]
    assert candidate.lang == "ja"
    assert str(candidate) == "分散"

    candidate = candidates[1]
    assert candidate.lang == "ja"
    assert str(candidate) == "分析ANOVA"
