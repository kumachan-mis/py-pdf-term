from abc import ABCMeta

from pytest import raises

from py_pdf_term.endtoend._endtoend.mappers import BaseMapper


class BaseTestMappedValue(metaclass=ABCMeta):
    __test__ = False

    def __init__(self, value: str) -> None:
        self.value = value


class TestDefaultMappedValue(BaseTestMappedValue):
    __test__ = False

    def __init__(self) -> None:
        super().__init__("Default")


class TestUserDefinedMappedValue(BaseTestMappedValue):
    __test__ = False

    def __init__(self) -> None:
        super().__init__("UserDefined")


class TestMapper(BaseMapper[type[BaseTestMappedValue]]):
    __test__ = False

    @classmethod
    def default_mapper(cls) -> BaseMapper[type[BaseTestMappedValue]]:
        mapper = cls()
        mapper.add("py_pdf_term.TestDefaultMappedValue", TestDefaultMappedValue)
        return mapper


def test_find() -> None:
    mapper = TestMapper.default_mapper()

    cls = mapper.find("py_pdf_term.TestDefaultMappedValue")
    assert cls == TestDefaultMappedValue

    raises(KeyError, lambda: mapper.find("py_pdf_term.TestUnknownMappedValue"))


def test_find_or_none() -> None:
    mapper = TestMapper.default_mapper()

    cls = mapper.find_or_none("py_pdf_term.TestDefaultMappedValue")
    assert cls == TestDefaultMappedValue

    cls = mapper.find_or_none("py_pdf_term.TestUnknownMappedValue")
    assert cls is None


def test_bulk_find() -> None:
    mapper = TestMapper.default_mapper()

    clses = mapper.bulk_find(["py_pdf_term.TestDefaultMappedValue"])
    assert clses == [TestDefaultMappedValue]

    raises(KeyError, lambda: mapper.bulk_find(["py_pdf_term.TestUnknownMappedValue"]))


def test_bulk_find_or_none() -> None:
    mapper = TestMapper.default_mapper()

    clses = mapper.bulk_find_or_none(
        [
            "py_pdf_term.TestDefaultMappedValue",
            "py_pdf_term.TestUserDefinedMappedValue",
            "py_pdf_term.TestUnknownMappedValue",
        ]
    )
    assert clses == [TestDefaultMappedValue, None, None]


def test_add_then_remove() -> None:
    mapper = TestMapper.default_mapper()

    cls = mapper.find("py_pdf_term.TestDefaultMappedValue")
    assert cls == TestDefaultMappedValue
    raises(KeyError, lambda: mapper.find("py_pdf_term.TestUserDefinedMappedValue"))

    mapper.add("py_pdf_term.TestUserDefinedMappedValue", TestUserDefinedMappedValue)

    cls = mapper.find("py_pdf_term.TestDefaultMappedValue")
    assert cls == TestDefaultMappedValue
    cls = mapper.find("py_pdf_term.TestUserDefinedMappedValue")
    assert cls == TestUserDefinedMappedValue

    mapper.remove("py_pdf_term.TestUserDefinedMappedValue")

    cls = mapper.find("py_pdf_term.TestDefaultMappedValue")
    assert cls == TestDefaultMappedValue
    raises(KeyError, lambda: mapper.find("py_pdf_term.TestUserDefinedMappedValue"))
