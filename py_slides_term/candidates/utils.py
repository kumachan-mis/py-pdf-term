from xml.etree.ElementTree import Element


def textnode_text(textnode: Element, default: str = "") -> str:
    return textnode.text or default


def textnode_fontsize(textnode: Element, default: float = 0.0) -> float:
    try:
        return float(textnode.get("size", default))
    except ValueError:
        return default
