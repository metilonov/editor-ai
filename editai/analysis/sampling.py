from __future__ import annotations

from collections.abc import Iterable

from editai.domain.models import TimeValue
from editai.utils.math import mean


def values_in_window(series: Iterable[TimeValue], start: float, end: float) -> list[float]:
    return [item.value for item in series if start <= item.time < end]


def window_mean(series: Iterable[TimeValue], start: float, end: float) -> float:
    return mean(values_in_window(series, start, end))


def normalize_series(series: list[TimeValue]) -> list[TimeValue]:
    if not series: return []
    vals = [x.value for x in series]; lo, hi = min(vals), max(vals)
    if hi-lo < 1e-12: return [TimeValue(x.time, 0.0) for x in series]
    return [TimeValue(x.time, (x.value-lo)/(hi-lo)) for x in series]
