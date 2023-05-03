from pathlib import Path

from py_pdf_term.candidates import PDFCandidateTermList
from py_pdf_term.configs import CandidateLayerConfig
from py_pdf_term.endtoend.caches import CandidateLayerFileCache, CandidateLayerNoCache


def test_file_cache(tmp_path: Path):
    cache = CandidateLayerFileCache(tmp_path.as_posix())

    pdf_path = "test.pdf"
    candidates = PDFCandidateTermList(pdf_path, [])
    config = CandidateLayerConfig()

    assert cache.load(pdf_path, config) is None

    cache.store(candidates, config)
    assert cache.load(pdf_path, config) == candidates

    cache.remove(pdf_path, config)
    assert cache.load(pdf_path, config) is None


def test_file_cache_doubled_operation(tmp_path: Path):
    cache = CandidateLayerFileCache(tmp_path.as_posix())

    pdf_path1 = "test1.pdf"
    candidates1 = PDFCandidateTermList(pdf_path1, [])
    pdf_path2 = "test2.pdf"
    candidates2 = PDFCandidateTermList(pdf_path2, [])
    config = CandidateLayerConfig()

    assert cache.load(pdf_path1, config) is None
    assert cache.load(pdf_path2, config) is None

    cache.store(candidates1, config)
    assert cache.load(pdf_path1, config) == candidates1
    assert cache.load(pdf_path2, config) is None

    cache.store(candidates2, config)
    assert cache.load(pdf_path1, config) == candidates1
    assert cache.load(pdf_path2, config) == candidates2

    cache.remove(pdf_path1, config)
    assert cache.load(pdf_path1, config) is None
    assert cache.load(pdf_path2, config) == candidates2

    cache.remove(pdf_path2, config)
    assert cache.load(pdf_path1, config) is None
    assert cache.load(pdf_path2, config) is None


def test_no_cache(tmp_path: Path):
    cache = CandidateLayerNoCache(tmp_path.as_posix())

    pdf_path = "test.pdf"
    candidates = PDFCandidateTermList(pdf_path, [])
    config = CandidateLayerConfig()

    assert cache.load(pdf_path, config) is None

    cache.store(candidates, config)
    assert cache.load(pdf_path, config) is None

    cache.remove(pdf_path, config)
    assert cache.load(pdf_path, config) is None
