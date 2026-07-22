from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from time import time
from typing import Any

from editai.domain.enums import JobStatus


@dataclass(slots=True)
class MediaInfo:
    path: Path
    duration: float
    width: int
    height: int
    fps: float
    size_bytes: int
    has_audio: bool
    video_codec: str = ""
    audio_codec: str = ""

    @property
    def aspect_ratio(self) -> float:
        return self.width / self.height if self.height else 0.0


@dataclass(slots=True)
class TimeValue:
    time: float
    value: float


@dataclass(slots=True)
class Scene:
    start: float
    end: float
    confidence: float = 1.0


@dataclass(slots=True)
class FeatureBundle:
    scenes: list[Scene] = field(default_factory=list)
    motion: list[TimeValue] = field(default_factory=list)
    audio_rms: list[TimeValue] = field(default_factory=list)
    audio_peaks: list[TimeValue] = field(default_factory=list)
    faces: list[TimeValue] = field(default_factory=list)
    sharpness: list[TimeValue] = field(default_factory=list)
    brightness: list[TimeValue] = field(default_factory=list)
    saturation: list[TimeValue] = field(default_factory=list)
    entropy: list[TimeValue] = field(default_factory=list)


@dataclass(slots=True)
class Candidate:
    start: float
    end: float
    features: dict[str, float] = field(default_factory=dict)
    score: float = 0.0
    reasons: list[str] = field(default_factory=list)

    @property
    def duration(self) -> float: return max(0.0, self.end - self.start)


@dataclass(slots=True)
class SubtitleSegment:
    start: float
    end: float
    text: str


@dataclass(slots=True)
class UserSettings:
    profile: str = "dynamic"
    clip_count: int = 3
    clip_duration: int = 30
    vertical_mode: str = "blur"
    subtitles: bool = False
    music: bool = False

    def to_dict(self) -> dict[str, Any]: return asdict(self)


@dataclass(slots=True)
class Job:
    id: str
    user_id: int
    chat_id: int
    source_kind: str
    source_value: str
    settings: UserSettings
    status: JobStatus = JobStatus.QUEUED
    created_at: float = field(default_factory=time)
    error: str | None = None
    input_path: Path | None = None
    outputs: list[Path] = field(default_factory=list)
