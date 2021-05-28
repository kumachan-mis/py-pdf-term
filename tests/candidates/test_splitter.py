from py_slides_term.candidates import CandidateTermExtractor


def test_japanese_backward_repeat_splitter() -> None:
    extractor = CandidateTermExtractor()
    candidates = extractor.extract_from_text("エントロピークロスエントロピー情報エントロピー")

    assert len(candidates) == 3

    candidate = candidates[0]
    assert candidate.lang == "ja"
    assert str(candidate) == "エントロピー"

    candidate = candidates[1]
    assert candidate.lang == "ja"
    assert str(candidate) == "クロスエントロピー"

    candidate = candidates[2]
    assert candidate.lang == "ja"
    assert str(candidate) == "情報エントロピー"


def test_japanese_forward_repeat_splitter() -> None:
    extractor = CandidateTermExtractor()
    candidates = extractor.extract_from_text("IPアドレスIPヘッダIP層")

    assert len(candidates) == 3

    candidate = candidates[0]
    assert candidate.lang == "ja"
    assert str(candidate) == "IPアドレス"

    candidate = candidates[1]
    assert candidate.lang == "ja"
    assert str(candidate) == "IPヘッダ"

    candidate = candidates[2]
    assert candidate.lang == "ja"
    assert str(candidate) == "IP層"


def test_japanese_bidirectional_repeat_splitter() -> None:
    extractor = CandidateTermExtractor()
    candidates = extractor.extract_from_text("ソフトウェア開発ソフトウェア工学要求工学")

    assert len(candidates) == 3

    candidate = candidates[0]
    assert candidate.lang == "ja"
    assert str(candidate) == "ソフトウェア開発"

    candidate = candidates[1]
    assert candidate.lang == "ja"
    assert str(candidate) == "ソフトウェア工学"

    candidate = candidates[2]
    assert candidate.lang == "ja"
    assert str(candidate) == "要求工学"


def test_english_backward_repeat_splitter() -> None:
    extractor = CandidateTermExtractor()
    candidates = extractor.extract_from_text(
        "black box testing white box testing gray box testing"
    )

    assert len(candidates) == 3

    candidate = candidates[0]
    assert candidate.lang == "en"
    assert str(candidate) == "black box testing"

    candidate = candidates[1]
    assert candidate.lang == "en"
    assert str(candidate) == "white box testing"

    candidate = candidates[2]
    assert candidate.lang == "en"
    assert str(candidate) == "gray box testing"


def test_english_forward_repeat_splitter() -> None:
    extractor = CandidateTermExtractor()
    candidates = extractor.extract_from_text(
        "lambda abstraction lambda calculus lambda expression"
    )

    assert len(candidates) == 3

    candidate = candidates[0]
    assert candidate.lang == "en"
    assert str(candidate) == "lambda abstraction"

    candidate = candidates[1]
    assert candidate.lang == "en"
    assert str(candidate) == "lambda calculus"

    candidate = candidates[2]
    assert candidate.lang == "en"
    assert str(candidate) == "lambda expression"


def test_english_bidirectional_repeat_splitter() -> None:
    extractor = CandidateTermExtractor()
    candidates = extractor.extract_from_text(
        "software development software engineering requirements engineering"
    )

    assert len(candidates) == 3

    candidate = candidates[0]
    assert candidate.lang == "en"
    assert str(candidate) == "software development"

    candidate = candidates[1]
    assert candidate.lang == "en"
    assert str(candidate) == "software engineering"

    candidate = candidates[2]
    assert candidate.lang == "en"
    assert str(candidate) == "requirements engineering"


def test_japanese_symname_splitter() -> None:
    extractor = CandidateTermExtractor()
    candidates = extractor.extract_from_text("ソフトウェア開発技術1")

    assert len(candidates) == 1

    candidate = candidates[0]
    assert candidate.lang == "ja"
    assert str(candidate) == "ソフトウェア開発技術"


def test_english_symname_splitter() -> None:
    extractor = CandidateTermExtractor()
    candidates = extractor.extract_from_text("Programming Language C")

    assert len(candidates) == 1

    candidate = candidates[0]
    assert candidate.lang == "en"
    assert str(candidate) == "Programming Language"
