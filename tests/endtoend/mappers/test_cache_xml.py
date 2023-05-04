from pytest import raises
from py_pdf_term.mappers import XMLLayerCacheMapper
from py_pdf_term.endtoend.caches import XMLLayerNoCache, XMLLayerFileCache


def test_default_mapper_find():
    mapper = XMLLayerCacheMapper.default_mapper()
    cls = mapper.find("py_pdf_term.XMLLayerNoCache")
    assert cls == XMLLayerNoCache
    cls = mapper.find("py_pdf_term.XMLLayerFileCache")
    assert cls == XMLLayerFileCache
    raises(KeyError, lambda: mapper.find("py_pdf_term.XMLLayerUnknownCache"))


def test_default_mapper_find_or_none():
    mapper = XMLLayerCacheMapper.default_mapper()
    cls = mapper.find_or_none("py_pdf_term.XMLLayerNoCache")
    assert cls == XMLLayerNoCache
    cls = mapper.find_or_none("py_pdf_term.XMLLayerFileCache")
    assert cls == XMLLayerFileCache
    cls = mapper.find_or_none("py_pdf_term.XMLLayerUnknownCache")
    assert cls is None


def test_default_mapper_bulk_find():
    mapper = XMLLayerCacheMapper.default_mapper()

    clses = mapper.bulk_find(
        ["py_pdf_term.XMLLayerNoCache", "py_pdf_term.XMLLayerFileCache"]
    )
    assert clses == [XMLLayerNoCache, XMLLayerFileCache]

    raises(KeyError, lambda: mapper.bulk_find(["py_pdf_term.XMLLayerUnknownCache"]))


def test_default_mapper_bulk_find_or_none():
    mapper = XMLLayerCacheMapper.default_mapper()

    clses = mapper.bulk_find_or_none(
        [
            "py_pdf_term.XMLLayerNoCache",
            "py_pdf_term.XMLLayerFileCache",
            "py_pdf_term.XMLLayerUnknownCache",
        ]
    )
    assert clses == [XMLLayerNoCache, XMLLayerFileCache, None]


def test_mapper_add_then_remove():
    mapper = XMLLayerCacheMapper()

    mapper.add("py_pdf_term.XMLLayerNoCache", XMLLayerNoCache)

    cls = mapper.find("py_pdf_term.XMLLayerNoCache")
    assert cls == XMLLayerNoCache

    mapper.remove("py_pdf_term.XMLLayerNoCache")
    raises(KeyError, lambda: mapper.find("py_pdf_term.XMLLayerNoCache"))
