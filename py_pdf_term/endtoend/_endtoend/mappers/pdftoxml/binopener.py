from typing import Type

from py_pdf_term.pdftoxml.binopener import BaseBinaryOpener, StandardBinaryOpener

from ..base import BaseMapper
from ..consts import PACKAGE_NAME


class BinaryOpenerMapper(BaseMapper[Type[BaseBinaryOpener]]):
    @classmethod
    def default_mapper(cls) -> "BinaryOpenerMapper":
        default_mapper = cls()

        binopener_clses = [StandardBinaryOpener]
        for binopener_cls in binopener_clses:
            default_mapper.add(
                f"{PACKAGE_NAME}.{binopener_cls.__name__}", binopener_cls
            )

        return default_mapper
