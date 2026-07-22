from __future__ import annotations

from pathlib import Path

from editai.domain.models import SubtitleSegment
from editai.utils.timecode import srt_time


def write_clip_srt(
    segments: list[SubtitleSegment], start: float, end: float, target: Path
) -> Path | None:
    selected: list[SubtitleSegment] = []
    for item in segments:
        if item.end <= start or item.start >= end:
            continue
        selected.append(
            SubtitleSegment(
                max(0.0, item.start - start),
                max(0.1, min(end, item.end) - start),
                item.text,
            )
        )
    if not selected:
        return None
    target.parent.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    for index, item in enumerate(selected, 1):
        lines.extend(
            [
                str(index),
                f"{srt_time(item.start)} --> {srt_time(item.end)}",
                item.text,
                "",
            ]
        )
    target.write_text("\n".join(lines), encoding="utf-8")
    return target
