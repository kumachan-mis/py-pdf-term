import re
from unicodedata import normalize
from typing import Optional

from py_slides_term.share.consts import FULLWIDTH_ASCII_CHARS, HALFWIDTH_ASCII_CHARS

CONTROL = re.compile(r"[\x00-\x08\x0b-\x0c\x0e-\x1f]")
SPACES = re.compile(r"\s+")
ERROR_TEXT = re.compile(r"\(cid:\d+\)")
ASCII_FULL2HALF_TABLE = str.maketrans(FULLWIDTH_ASCII_CHARS, HALFWIDTH_ASCII_CHARS)


def clean_content_text(
    text: str,
    stripcontrol: bool,
    nfc_norm: bool,
    include_pattern: Optional[str],
) -> str:
    if stripcontrol:
        text = CONTROL.sub("", text)
    if nfc_norm:
        text = normalize("NFC", text)

    text = SPACES.sub(" ", text).strip()
    text = text.translate(ASCII_FULL2HALF_TABLE)

    return text if include_pattern is None or re.search(include_pattern, text) else ""
