from py_pdf_term.analysis import TermOccurrenceAnalyzer
from py_pdf_term.candidates import (
    CandidateTermExtractor,
    DomainCandidateTermList,
    PDFCandidateTermList,
    PageCandidateTermList,
)


def test_term_occ_with_no_subterm() -> None:
    extractor = CandidateTermExtractor()
    analyzer = TermOccurrenceAnalyzer()
    candidates = extractor.extract_from_text(
        "[線形識別 (Linear Classification) とパーセプトロン (Perceptron)]"
        + "特徴空間を超平面で分割してクラス識別を行うのが線形識別である。"
        + "線形識別はパーセプトロンとしてモデル化される。"
    )
    expected_candidates_lemma = [
        "線形識別",
        "linear classification",
        "パーセプトロン",
        "perceptron",
        "特徴空間",
        "超平面",
        "分割",
        "クラス識別",
        "線形識別",
        "線形識別",
        "パーセプトロン",
        "モデル化",
    ]
    assert list(map(lambda c: c.lemma(), candidates)) == expected_candidates_lemma

    result = analyzer.analyze(
        DomainCandidateTermList(
            "test",
            [
                PDFCandidateTermList(
                    "test/test.pdf",
                    [
                        PageCandidateTermList(1, candidates),
                    ],
                )
            ],
        )
    )
    expected_doc_term_freq = {
        "線形識別": 1,
        "linear classification": 1,
        "パーセプトロン": 1,
        "perceptron": 1,
        "特徴空間": 1,
        "超平面": 1,
        "分割": 1,
        "クラス識別": 1,
        "モデル化": 1,
    }
    expected_term_freq = {
        "線形識別": 3,
        "linear classification": 1,
        "パーセプトロン": 2,
        "perceptron": 1,
        "特徴空間": 1,
        "超平面": 1,
        "分割": 1,
        "クラス識別": 1,
        "モデル化": 1,
    }
    assert result.domain == "test"
    assert result.doc_term_freq == expected_doc_term_freq
    assert result.term_freq == expected_term_freq


def test_term_occ_with_subterm() -> None:
    extractor = CandidateTermExtractor()
    analyzer = TermOccurrenceAnalyzer()
    candidates = extractor.extract_from_text(
        "子を持たないノードを葉ないし外部ノード (external node) と呼ぶ。"
        + "葉でないノードを内部ノード (internal node) と呼ぶ。"
        + "あるノードの深さはルートからそのノードまでにたどる経路の長さである。"
    )
    expected_candidates_lemma = [
        "子",
        "ノード",
        "葉",
        "外部ノード",
        "external node",
        "葉",
        "ノード",
        "内部ノード",
        "internal node",
        "ノード",
        "深いさ",
        "ノードの深いさ",
        "ルート",
        "ノード",
        "経路",
        "長いさ",
        "経路の長いさ",
    ]
    assert list(map(lambda c: c.lemma(), candidates)) == expected_candidates_lemma

    result = analyzer.analyze(
        DomainCandidateTermList(
            "test",
            [
                PDFCandidateTermList(
                    "test/test.pdf",
                    [
                        PageCandidateTermList(1, candidates),
                    ],
                )
            ],
        )
    )
    expected_doc_term_freq = {
        "子": 1,
        "ノード": 1,
        "葉": 1,
        "外部ノード": 1,
        "external node": 1,
        "内部ノード": 1,
        "internal node": 1,
        "深いさ": 1,
        "ノードの深いさ": 1,
        "ルート": 1,
        "経路": 1,
        "長いさ": 1,
        "経路の長いさ": 1,
    }
    expected_term_freq = {
        "子": 1,
        "ノード": 6,
        "葉": 2,
        "外部ノード": 1,
        "external node": 1,
        "内部ノード": 1,
        "internal node": 1,
        "深いさ": 1,
        "ノードの深いさ": 1,
        "ルート": 1,
        "経路": 1,
        "長いさ": 1,
        "経路の長いさ": 1,
    }
    assert result.domain == "test"
    assert result.doc_term_freq == expected_doc_term_freq
    assert result.term_freq == expected_term_freq


def test_term_occ_with_augmented() -> None:
    extractor = CandidateTermExtractor()
    analyzer = TermOccurrenceAnalyzer(ignore_augmented=False)
    candidates = extractor.extract_from_text("ローカル変数とグローバル変数での変数の値の評価")
    expected_candidates_lemma = [
        "ローカル変数",
        "グローバル変数",
        "変数",
        "値",
        "評価",
        "変数の値",
        "値の評価",
        "変数の値の評価",
    ]
    assert list(map(lambda c: c.lemma(), candidates)) == expected_candidates_lemma

    result = analyzer.analyze(
        DomainCandidateTermList(
            "test",
            [
                PDFCandidateTermList(
                    "test/test.pdf",
                    [
                        PageCandidateTermList(1, candidates),
                    ],
                )
            ],
        )
    )
    expected_doc_term_freq = {
        "ローカル変数": 1,
        "グローバル変数": 1,
        "変数": 1,
        "値": 1,
        "評価": 1,
        "変数の値": 1,
        "値の評価": 1,
        "変数の値の評価": 1,
    }
    expected_term_freq = {
        "ローカル変数": 1,
        "グローバル変数": 1,
        "変数": 5,
        "値": 4,
        "評価": 3,
        "変数の値": 2,
        "値の評価": 2,
        "変数の値の評価": 1,
    }
    assert result.domain == "test"
    assert result.doc_term_freq == expected_doc_term_freq
    assert result.term_freq == expected_term_freq
