from __future__ import annotations

from collections.abc import Iterable


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def normalize(values: Iterable[float]) -> list[float]:
    data = list(values)
    if not data: return []
    lo, hi = min(data), max(data)
    if hi - lo < 1e-12: return [0.0 for _ in data]
    return [(v - lo) / (hi - lo) for v in data]


def mean(values: Iterable[float], default: float = 0.0) -> float:
    data = list(values)
    return sum(data) / len(data) if data else default


def overlap_ratio(a_start: float, a_end: float, b_start: float, b_end: float) -> float:
    overlap = max(0.0, min(a_end, b_end) - max(a_start, b_start))
    denom = max(1e-9, min(a_end-a_start, b_end-b_start))
    return overlap / denom
