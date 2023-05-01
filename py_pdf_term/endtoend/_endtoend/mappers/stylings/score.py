from typing import Type

from py_pdf_term._common.consts import PACKAGE_NAME
from py_pdf_term.stylings.scores import BaseStylingScore, ColorScore, FontsizeScore

from ..base import BaseMapper


class StylingScoreMapper(BaseMapper[Type[BaseStylingScore]]):
    """A mapper to find styling score classes."""

    @classmethod
    def default_mapper(cls) -> "StylingScoreMapper":
        default_mapper = cls()

        styling_score_clses = [FontsizeScore, ColorScore]
        for styling_score_cls in styling_score_clses:
            default_mapper.add(
                f"{PACKAGE_NAME}.{styling_score_cls.__name__}", styling_score_cls
            )

        return default_mapper
