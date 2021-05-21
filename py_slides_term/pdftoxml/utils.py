import re
from unicodedata import normalize
from typing import Optional

from py_slides_term.share.consts import FULLWIDTH_ASCII_CHARS, HALFWIDTH_ASCII_CHARS

CONTROL = re.compile(r"[\x00-\x08\x0b-\x0c\x0e-\x1f]")
ERROR = re.compile(r"\(cid:\d+\)")
SPACES = re.compile(r"\s+")
ASCII_FULL2HALF_TABLE = str.maketrans(FULLWIDTH_ASCII_CHARS, HALFWIDTH_ASCII_CHARS)


def clean_content_text(
    text: str,
    nfc_norm: bool,
    include_pattern: Optional[str],
    exclude_parrern: Optional[str],
) -> str:
    text = CONTROL.sub("", text)
    text = ERROR.sub("", text)
    text = SPACES.sub(" ", text).strip()
    text = text.translate(ASCII_FULL2HALF_TABLE)

    if nfc_norm:
        text = normalize("NFC", text)

    return (
        text
        if (include_pattern is None or re.search(include_pattern, text) is not None)
        and (exclude_parrern is None or re.search(exclude_parrern, text) is None)
        else ""
    )
