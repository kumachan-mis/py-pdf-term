from math import log, log2, log10
from typing import SupportsFloat


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
