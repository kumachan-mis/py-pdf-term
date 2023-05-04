from pytest import raises
from py_pdf_term.mappers import CandidateLayerCacheMapper
from py_pdf_term.endtoend.caches import CandidateLayerNoCache, CandidateLayerFileCache


def test_default_mapper_find():
    mapper = CandidateLayerCacheMapper.default_mapper()

    cls = mapper.find("py_pdf_term.CandidateLayerNoCache")
    assert cls == CandidateLayerNoCache
    cls = mapper.find("py_pdf_term.CandidateLayerFileCache")
    assert cls == CandidateLayerFileCache

    raises(KeyError, lambda: mapper.find("py_pdf_term.CandidateLayerUnknownCache"))


def test_default_mapper_find_or_none():
    mapper = CandidateLayerCacheMapper.default_mapper()

    cls = mapper.find_or_none("py_pdf_term.CandidateLayerNoCache")
    assert cls == CandidateLayerNoCache
    cls = mapper.find_or_none("py_pdf_term.CandidateLayerFileCache")
    assert cls == CandidateLayerFileCache
    cls = mapper.find_or_none("py_pdf_term.CandidateLayerUnknownCache")
    assert cls is None


def test_default_mapper_bulk_find():
    mapper = CandidateLayerCacheMapper.default_mapper()

    clses = mapper.bulk_find(
        ["py_pdf_term.CandidateLayerNoCache", "py_pdf_term.CandidateLayerFileCache"]
    )
    assert clses == [CandidateLayerNoCache, CandidateLayerFileCache]

    raises(
        KeyError, lambda: mapper.bulk_find(["py_pdf_term.CandidateLayerUnknownCache"])
    )


def test_default_mapper_bulk_find_or_none():
    mapper = CandidateLayerCacheMapper.default_mapper()

    clses = mapper.bulk_find_or_none(
        [
            "py_pdf_term.CandidateLayerNoCache",
            "py_pdf_term.CandidateLayerFileCache",
            "py_pdf_term.CandidateLayerUnknownCache",
        ]
    )
    assert clses == [CandidateLayerNoCache, CandidateLayerFileCache, None]


def test_mapper_add_then_remove():
    mapper = CandidateLayerCacheMapper()

    mapper.add("py_pdf_term.CandidateLayerNoCache", CandidateLayerNoCache)

    cls = mapper.find("py_pdf_term.CandidateLayerNoCache")
    assert cls == CandidateLayerNoCache

    mapper.remove("py_pdf_term.CandidateLayerNoCache")

    raises(KeyError, lambda: mapper.find("py_pdf_term.CandidateLayerNoCache"))
