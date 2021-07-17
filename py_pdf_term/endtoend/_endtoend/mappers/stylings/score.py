from typing import Type

from ..base import BaseMapper
from ..consts import PACKAGE_NAME
from py_pdf_term.stylings import BaseStylingScore, FontsizeScore, ColorScore


class StylingScoreMapper(BaseMapper[Type[BaseStylingScore]]):
    @classmethod
    def default_mapper(cls) -> "StylingScoreMapper":
        default_mapper = cls()

        styling_score_clses = [FontsizeScore, ColorScore]
        for styling_score_cls in styling_score_clses:
            default_mapper.add(
                f"{PACKAGE_NAME}.{styling_score_cls.__name__}", styling_score_cls
            )

        return default_mapper
