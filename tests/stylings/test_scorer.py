from py_pdf_term.candidates import (
    CandidateTermExtractor,
    PageCandidateTermList,
    PDFCandidateTermList,
)
from py_pdf_term.stylings import StylingScorer


def test_fontsize_score() -> None:
    extractor = CandidateTermExtractor()
    scorer = StylingScorer()
    candidates = (
        extractor.extract_from_text(
            "決定木",
            fontsize=28,
        )
        + extractor.extract_from_text(
            "決定理論において決定を行うためのグラフである。意思決定を助ける目的で作られる。",
            fontsize=20,
        )
        + extractor.extract_from_text(
            "c.f. グラフ、決定表",
            fontsize=14,
        )
    )
    candidates_sized_lemma = [(c.lemma(), c.fontsize) for c in candidates]
    expected_candidates_sized_lemma = [
        ("決定木", 28),
        ("決定理論", 20),
        ("決定", 20),
        ("グラフ", 20),
        ("意思決定", 20),
        ("目的", 20),
        ("グラフ", 14),
        ("決定表", 14),
    ]
    assert candidates_sized_lemma == expected_candidates_sized_lemma

    pdf_styling_scores = scorer.score_pdf_candidates(
        PDFCandidateTermList("test/test.pdf", [PageCandidateTermList(1, candidates)])
    )
    assert pdf_styling_scores.pdf_path == "test/test.pdf"
    assert len(pdf_styling_scores.pages) == 1

    page = pdf_styling_scores.pages[0]
    expected_term_set = set(map(lambda p: p[0], expected_candidates_sized_lemma))
    assert page.page_num == 1
    assert len(page.ranking) == len(expected_term_set)
    assert set(map(lambda e: e.term, page.ranking)) == expected_term_set
    assert page.ranking == sorted(page.ranking, key=lambda e: e.score, reverse=True)

    term_score_dict = dict(map(lambda e: (e.term, e.score), page.ranking))
    assert term_score_dict["決定木"] >= term_score_dict["決定理論"]
    # larger term should be scored higher (1)
    assert term_score_dict["決定理論"] >= term_score_dict["決定表"]
    # larger term should be scored higher (2)
    assert abs(term_score_dict["決定理論"] - term_score_dict["グラフ"]) < 1e-4
    # even if smaller fontsized term appears, it doesn't have any effect on the score


def test_color_score() -> None:
    extractor = CandidateTermExtractor()
    scorer = StylingScorer()
    candidates = extractor.extract_from_text(
        "決定木と決定理論",
        ncolor=str((1.0, 0.0, 0.0)),
    ) + extractor.extract_from_text(
        "決定理論において決定を行うためのグラフである。意思決定を助ける目的で作られる。",
        ncolor=str((0.0, 0.0, 0.0)),
    )
    candidates_colored_lemma = [(c.lemma(), c.ncolor) for c in candidates]
    expected_candidates_colored_lemma = [
        ("決定木", str((1.0, 0.0, 0.0))),
        ("決定理論", str((1.0, 0.0, 0.0))),
        ("決定理論", str((0.0, 0.0, 0.0))),
        ("決定", str((0.0, 0.0, 0.0))),
        ("グラフ", str((0.0, 0.0, 0.0))),
        ("意思決定", str((0.0, 0.0, 0.0))),
        ("目的", str((0.0, 0.0, 0.0))),
    ]
    assert candidates_colored_lemma == expected_candidates_colored_lemma

    pdf_styling_scores = scorer.score_pdf_candidates(
        PDFCandidateTermList("test/test.pdf", [PageCandidateTermList(1, candidates)])
    )
    assert pdf_styling_scores.pdf_path == "test/test.pdf"
    assert len(pdf_styling_scores.pages) == 1

    page = pdf_styling_scores.pages[0]
    expected_term_set = set(map(lambda p: p[0], expected_candidates_colored_lemma))
    assert page.page_num == 1
    assert len(page.ranking) == len(expected_term_set)
    assert set(map(lambda e: e.term, page.ranking)) == expected_term_set
    assert page.ranking == sorted(page.ranking, key=lambda e: e.score, reverse=True)

    term_score_dict = dict(map(lambda e: (e.term, e.score), page.ranking))
    assert term_score_dict["決定木"] >= term_score_dict["決定"]
    # rare-colored term should be scored higher
    assert abs(term_score_dict["決定木"] - term_score_dict["決定理論"]) < 1e-4
    # even if common-colored term appears, it doesn't have any effect on the score


def test_mixed_score() -> None:
    extractor = CandidateTermExtractor()
    scorer = StylingScorer()

    candidates = (
        extractor.extract_from_text(
            "決定木",
            fontsize=28,
            ncolor=str((1.0, 0.0, 0.0)),
        )
        + extractor.extract_from_text(
            "決定表",
            fontsize=28,
            ncolor=str((0.0, 0.0, 0.0)),
        )
        + extractor.extract_from_text(
            "決定理論において決定を行うためのグラフである。意思決定を助ける目的で作られる。",
            fontsize=20,
            ncolor=str((0.0, 0.0, 0.0)),
        )
        + extractor.extract_from_text(
            "リスクマネジメント",
            fontsize=20,
            ncolor=str((1.0, 0.0, 0.0)),
        )
    )
    candidates_mixed_lemma = [(c.lemma(), c.fontsize, c.ncolor) for c in candidates]
    expected_candidates_mixed_lemma = [
        ("決定木", 28, str((1.0, 0.0, 0.0))),
        ("決定表", 28, str((0.0, 0.0, 0.0))),
        ("決定理論", 20, str((0.0, 0.0, 0.0))),
        ("決定", 20, str((0.0, 0.0, 0.0))),
        ("グラフ", 20, str((0.0, 0.0, 0.0))),
        ("意思決定", 20, str((0.0, 0.0, 0.0))),
        ("目的", 20, str((0.0, 0.0, 0.0))),
        ("リスクマネジメント", 20, str((1.0, 0.0, 0.0))),
    ]
    assert candidates_mixed_lemma == expected_candidates_mixed_lemma

    pdf_styling_scores = scorer.score_pdf_candidates(
        PDFCandidateTermList("test/test.pdf", [PageCandidateTermList(1, candidates)])
    )
    assert pdf_styling_scores.pdf_path == "test/test.pdf"
    assert len(pdf_styling_scores.pages) == 1

    page = pdf_styling_scores.pages[0]
    expected_term_set = set(map(lambda t: t[0], expected_candidates_mixed_lemma))
    assert page.page_num == 1
    assert len(page.ranking) == len(expected_term_set)
    assert set(map(lambda e: e.term, page.ranking)) == expected_term_set
    assert page.ranking == sorted(page.ranking, key=lambda e: e.score, reverse=True)

    term_score_dict = dict(map(lambda e: (e.term, e.score), page.ranking))
    assert term_score_dict["決定木"] >= term_score_dict["決定表"]
    # rare-colored term should be scored higher (1)
    assert term_score_dict["決定木"] >= term_score_dict["リスクマネジメント"]
    # larger term should be scored higher (1)
    assert term_score_dict["決定表"] >= term_score_dict["意思決定"]
    # larger term should be scored higher (2)
    assert term_score_dict["リスクマネジメント"] >= term_score_dict["意思決定"]
    # rare-colored term should be scored higher (2)
