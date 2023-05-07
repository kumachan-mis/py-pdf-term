from math import log10
from typing import SupportsFloat


def extended_log10(__x: SupportsFloat) -> float:
    float_x = float(__x)
    if float_x > 0.0:
        return log10(float_x + 1.0)
    if float_x < 0.0:
        return -log10(-float_x + 1.0)
    else:
        return 0.0
