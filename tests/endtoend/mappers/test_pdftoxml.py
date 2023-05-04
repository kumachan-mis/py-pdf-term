from py_pdf_term.mappers import BinaryOpenerMapper
from py_pdf_term.pdftoxml.binopeners import StandardBinaryOpener


def test_binary_opener_default_mapper():
    mapper = BinaryOpenerMapper.default_mapper()

    clses = mapper.bulk_find_or_none(
        [
            "py_pdf_term.StandardBinaryOpener",
            "py_pdf_term.UnknownBinaryOpener",
        ]
    )
    assert clses == [StandardBinaryOpener, None]
