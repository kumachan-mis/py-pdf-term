from typing import List, SupportsFloat, TypeVar
from math import log, log2, log10

__T = TypeVar("__T")


def extended_log(x: SupportsFloat, base: SupportsFloat) -> float:
    float_x = float(x)
    if float_x > 0.0:
        return log(float_x + 1.0, base)
    if float_x < 0.0:
        return -log(-float_x + 1.0, base)
    else:
        return 0.0


def extended_log2(__x: SupportsFloat) -> float:
    float_x = float(__x)
    if float_x > 0.0:
        return log2(float_x + 1.0)
    if float_x < 0.0:
        return -log2(-float_x + 1.0)
    else:
        return 0.0


def extended_log10(__x: SupportsFloat) -> float:
    float_x = float(__x)
    if float_x > 0.0:
        return log10(float_x + 1.0)
    if float_x < 0.0:
        return -log10(-float_x + 1.0)
    else:
        return 0.0


def remove_duplicated_items(__ls: List[__T]) -> List[__T]:
    return list(
        map(
            lambda enumitem: enumitem[1],
            filter(
                lambda enumitem: enumitem[0] == __ls.index(enumitem[1]),
                enumerate(__ls),
            ),
        )
    )
