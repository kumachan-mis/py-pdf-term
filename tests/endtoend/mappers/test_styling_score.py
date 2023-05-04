from py_pdf_term.mappers import StylingScoreMapper
from py_pdf_term.stylings.scores import ColorScore, FontsizeScore


def test_styling_score_default_mapper():
    mapper = StylingScoreMapper.default_mapper()

    clses = mapper.bulk_find_or_none(
        [
            "py_pdf_term.ColorScore",
            "py_pdf_term.FontsizeScore",
            "py_pdf_term.UnknownBinaryOpener",
        ]
    )
    assert clses == [ColorScore, FontsizeScore, None]
