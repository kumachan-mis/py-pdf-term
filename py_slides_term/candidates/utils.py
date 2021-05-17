import re
from xml.etree.ElementTree import Element

FLOAT_REGEX = r"\d+(?:\.\d+)?"
BRACKET_MONO_REGEX = rf"\[({FLOAT_REGEX})\]"
PAREN_MONO_REGEX = rf"\(({FLOAT_REGEX})\)"
BRACKET_TRI_REGEX = rf"\[({FLOAT_REGEX})\s*,\s*({FLOAT_REGEX})\s*,\s*({FLOAT_REGEX})\]"
PAREN_TRI_REGEX = rf"\(({FLOAT_REGEX})\s*,\s*({FLOAT_REGEX})\s*,\s*({FLOAT_REGEX})\)"


def textnode_text(textnode: Element, default: str = "") -> str:
    return textnode.text or default


def textnode_fontsize(textnode: Element, default: float = 0.0) -> float:
    try:
        return float(textnode.get("size", default))
    except ValueError:
        return default


def textnode_ncolor(textnode: Element, default: str = str((0.0, 0.0, 0.0))) -> str:
    raw_ncolor = textnode.get("ncolor")
    if raw_ncolor is None:
        return default

    match = re.fullmatch(FLOAT_REGEX, raw_ncolor)
    if match:
        color = float(match[0])
        return str((color, color, color))

    match = re.fullmatch(BRACKET_MONO_REGEX, raw_ncolor)
    if match:
        color = float(match[1])
        return str((color, color, color))

    match = re.fullmatch(PAREN_MONO_REGEX, raw_ncolor)
    if match:
        color = float(match[1])
        return str((color, color, color))

    match = re.fullmatch(BRACKET_TRI_REGEX, raw_ncolor)
    if match:
        color = float(match[1]), float(match[2]), float(match[3])
        return str(color)

    match = re.fullmatch(PAREN_TRI_REGEX, raw_ncolor)
    if match:
        color = float(match[1]), float(match[2]), float(match[3])
        return str(color)

    return default
