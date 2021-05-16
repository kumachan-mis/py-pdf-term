# http://www.shurey.com/js/works/unicode.html

# Alphabet
ALPHABET_REGEX = r"[A-Za-z]"

# Hiragana
HIRAGANA_REGEX = r"[\u3040-\u309F]"

# Katakana
KATAKANA_REGEX = r"[\u30A0-\u30FF]"

# CJK Radicals Supplement
# Kangxi Radicals
# CJK Unified Ideographs Extension A
# CJK Unified Ideographs
# CJK Compatibility Ideographs
KANJI_REGEX = r"[\u2E80-\u2EFF\u2F00-\u2FDF\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF]"

JAPANESE_REGEX = rf"(?:{HIRAGANA_REGEX}|{KATAKANA_REGEX}|{KANJI_REGEX})"

SYMBOL_REGEX = (
    "["
    + "".join(
        [
            # Basic Latin Symbol
            "\u0020-\u002F",
            "\u003A-\u0040",
            "\u005B-\u0060",
            "\u007B-\u007F",
            # Latin-1 Supplement Symbol
            "\u00A1-\u00BF\u00D7\u00F7",
            # Spacing Modifier Letters - Combining Diacritical Marks
            "\u02B0-\u036F",
            # Phonetic Extensions - Combining Diacritical Marks Supplement
            "\u1D00-\u1DFF",
            # General Punctuation - Miscellaneous Symbols and Arrows
            "\u2010-\u2BFF",
            # Supplemental Punctuation
            "\u2E00-\u2E7F",
            # Ideographic Description Characters - CJK Symbols and Punctuation
            "\u2FF0-\u303F"
            # Bopomofo - CJK Strokes
            "\u3100-\u31EF",
            # Enclosed CJK Letters and Months - CJK Compatibility
            "\u3200-\u33FF",
            # Yijing Hexagram Symbols
            "\u4DC0-\u4DFF",
            # Modifier Tone Letters
            "\uA700-\uA71F",
            # High Surrogates - Private Use Area
            "\uD800-\uF8FF",
            # Variation Selectors - Small Form Variants
            "\uFE00-\uFE6F",
            # Specials
            "\uFFF0-\uFFFF",
        ]
    )
    + "]"
)
