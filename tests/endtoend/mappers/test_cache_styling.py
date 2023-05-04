from pytest import raises
from py_pdf_term.mappers import StylingLayerCacheMapper
from py_pdf_term.endtoend.caches import StylingLayerNoCache, StylingLayerFileCache


def test_default_mapper_find():
    mapper = StylingLayerCacheMapper.default_mapper()

    cls = mapper.find("py_pdf_term.StylingLayerNoCache")
    assert cls == StylingLayerNoCache
    cls = mapper.find("py_pdf_term.StylingLayerFileCache")
    assert cls == StylingLayerFileCache

    raises(KeyError, lambda: mapper.find("py_pdf_term.StylingLayerUnknownCache"))


def test_default_mapper_find_or_none():
    mapper = StylingLayerCacheMapper.default_mapper()

    cls = mapper.find_or_none("py_pdf_term.StylingLayerNoCache")
    assert cls == StylingLayerNoCache
    cls = mapper.find_or_none("py_pdf_term.StylingLayerFileCache")
    assert cls == StylingLayerFileCache
    cls = mapper.find_or_none("py_pdf_term.StylingLayerUnknownCache")
    assert cls is None


def test_default_mapper_bulk_find():
    mapper = StylingLayerCacheMapper.default_mapper()

    clses = mapper.bulk_find(
        ["py_pdf_term.StylingLayerNoCache", "py_pdf_term.StylingLayerFileCache"]
    )
    assert clses == [StylingLayerNoCache, StylingLayerFileCache]

    raises(KeyError, lambda: mapper.bulk_find(["py_pdf_term.StylingLayerUnknownCache"]))


def test_default_mapper_bulk_find_or_none():
    mapper = StylingLayerCacheMapper.default_mapper()

    clses = mapper.bulk_find_or_none(
        [
            "py_pdf_term.StylingLayerNoCache",
            "py_pdf_term.StylingLayerFileCache",
            "py_pdf_term.StylingLayerUnknownCache",
        ]
    )
    assert clses == [StylingLayerNoCache, StylingLayerFileCache, None]


def test_mapper_add_then_remove():
    mapper = StylingLayerCacheMapper()

    mapper.add("py_pdf_term.StylingLayerNoCache", StylingLayerNoCache)

    cls = mapper.find("py_pdf_term.StylingLayerNoCache")
    assert cls == StylingLayerNoCache

    mapper.remove("py_pdf_term.StylingLayerNoCache")
    raises(KeyError, lambda: mapper.find("py_pdf_term.StylingLayerNoCache"))
