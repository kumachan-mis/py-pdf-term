from typing import Self

from py_pdf_term._common.consts import PACKAGE_NAME
from py_pdf_term.pdftoxml.binopeners import BaseBinaryOpener, StandardBinaryOpener

from ..base import BaseMapper


class BinaryOpenerMapper(BaseMapper[type[BaseBinaryOpener]]):
    """Mapper to find binary opener classes."""

    @classmethod
    def default_mapper(cls) -> Self:
        default_mapper = cls()

        binopener_clses: list[type[BaseBinaryOpener]] = [StandardBinaryOpener]
        for binopener_cls in binopener_clses:
            default_mapper.add(
                f"{PACKAGE_NAME}.{binopener_cls.__name__}", binopener_cls
            )

        return default_mapper
