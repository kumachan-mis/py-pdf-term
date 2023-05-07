from pathlib import Path

from py_pdf_term._common.data import ScoredTerm
from py_pdf_term.configs import StylingLayerConfig
from py_pdf_term.endtoend.caches import StylingLayerFileCache, StylingLayerNoCache
from py_pdf_term.stylings import PageStylingScoreList, PDFStylingScoreList


def test_file_cache(tmp_path: Path):
    cache = StylingLayerFileCache(tmp_path.as_posix())

    pdf_path = "test.pdf"
    first_styling_scores = PDFStylingScoreList(
        pdf_path,
        [
            PageStylingScoreList(
                1,
                [
                    ScoredTerm("rare term", 2.0),
                    ScoredTerm("technical term", 1.0),
                    ScoredTerm("common word", 0.5),
                ],
            )
        ],
    )
    second_styling_scores = PDFStylingScoreList(
        pdf_path,
        [
            PageStylingScoreList(
                1,
                [
                    ScoredTerm("rare term", 5.0),
                    ScoredTerm("technical term", 2.5),
                    ScoredTerm("common word", 0.0),
                ],
            )
        ],
    )
    config = StylingLayerConfig()

    assert cache.load(pdf_path, config) is None

    cache.store(first_styling_scores, config)
    assert cache.load(pdf_path, config) == first_styling_scores

    cache.store(second_styling_scores, config)
    assert cache.load(pdf_path, config) == second_styling_scores

    cache.remove(pdf_path, config)
    assert cache.load(pdf_path, config) is None

    cache.remove(pdf_path, config)
    assert cache.load(pdf_path, config) is None


def test_file_cache_multiple(tmp_path: Path):
    cache = StylingLayerFileCache(tmp_path.as_posix())

    pdf_path1 = "test1.pdf"
    styling_scores1 = PDFStylingScoreList(
        pdf_path1,
        [
            PageStylingScoreList(
                1,
                [
                    ScoredTerm("rare term", 2.0),
                    ScoredTerm("technical term", 1.0),
                    ScoredTerm("common word", 0.5),
                ],
            )
        ],
    )
    pdf_path2 = "test2.pdf"
    styling_scores2 = PDFStylingScoreList(
        pdf_path2,
        [
            PageStylingScoreList(
                1,
                [
                    ScoredTerm("rare term", 5.0),
                    ScoredTerm("technical term", 2.5),
                    ScoredTerm("common word", 0.0),
                ],
            )
        ],
    )
    config = StylingLayerConfig()

    assert cache.load(pdf_path1, config) is None
    assert cache.load(pdf_path2, config) is None

    cache.store(styling_scores1, config)
    assert cache.load(pdf_path1, config) == styling_scores1
    assert cache.load(pdf_path2, config) is None

    cache.store(styling_scores2, config)
    assert cache.load(pdf_path1, config) == styling_scores1
    assert cache.load(pdf_path2, config) == styling_scores2

    cache.remove(pdf_path1, config)
    assert cache.load(pdf_path1, config) is None
    assert cache.load(pdf_path2, config) == styling_scores2

    cache.remove(pdf_path2, config)
    assert cache.load(pdf_path1, config) is None
    assert cache.load(pdf_path2, config) is None


def test_no_cache(tmp_path: Path):
    cache = StylingLayerNoCache(tmp_path.as_posix())

    pdf_path = "test.pdf"
    first_styling_scores = PDFStylingScoreList(
        pdf_path,
        [
            PageStylingScoreList(
                1,
                [
                    ScoredTerm("rare term", 2.0),
                    ScoredTerm("technical term", 1.0),
                    ScoredTerm("common word", 0.5),
                ],
            )
        ],
    )
    second_styling_scores = PDFStylingScoreList(
        pdf_path,
        [
            PageStylingScoreList(
                1,
                [
                    ScoredTerm("rare term", 5.0),
                    ScoredTerm("technical term", 2.5),
                    ScoredTerm("common word", 0.0),
                ],
            )
        ],
    )
    config = StylingLayerConfig()

    assert cache.load(pdf_path, config) is None

    cache.store(first_styling_scores, config)
    assert cache.load(pdf_path, config) is None

    cache.store(second_styling_scores, config)
    assert cache.load(pdf_path, config) is None

    cache.remove(pdf_path, config)
    assert cache.load(pdf_path, config) is None

    cache.remove(pdf_path, config)
    assert cache.load(pdf_path, config) is None
