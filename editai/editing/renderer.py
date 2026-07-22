from __future__ import annotations

from pathlib import Path

from editai.domain.models import Candidate
from editai.domain.profiles import EditProfile
from editai.editing.filtergraph import build_video_filter
from editai.media.process import run_process


def _atempo_chain(speed: float) -> str:
    value = max(0.5, min(2.0, speed))
    return f"atempo={value:.4f}"


async def render_clip(
    source: Path,
    candidate: Candidate,
    target: Path,
    profile: EditProfile,
    vertical_mode: str,
    subtitle: Path | None,
    music: Path | None,
    has_audio: bool,
) -> Path:
    target.parent.mkdir(parents=True, exist_ok=True)
    duration = candidate.duration
    output_duration = duration / max(profile.speed, 0.01)
    video_filter = build_video_filter(
        vertical_mode, profile, duration, str(subtitle) if subtitle else None
    )

    args = [
        "ffmpeg", "-y", "-ss", f"{candidate.start:.3f}", "-t", f"{duration:.3f}",
        "-i", str(source),
    ]
    if music:
        args += ["-stream_loop", "-1", "-i", str(music)]

    graph_parts = [f"[0:v]{video_filter}[v]"]
    audio_map: str | None = None
    if music and has_audio:
        graph_parts.extend(
            [
                f"[0:a]{_atempo_chain(profile.speed)},volume=1.0[srca]",
                f"[1:a]atrim=0:{output_duration:.3f},asetpts=N/SR/TB,volume=0.16,"
                f"afade=t=out:st={max(0.0, output_duration - 0.8):.3f}:d=0.8[music]",
                "[srca][music]amix=inputs=2:duration=first:dropout_transition=2,"
                "loudnorm=I=-16:TP=-1.5:LRA=11[a]",
            ]
        )
        audio_map = "[a]"
    elif music:
        graph_parts.append(
            f"[1:a]atrim=0:{output_duration:.3f},asetpts=N/SR/TB,volume=0.28,"
            f"afade=t=out:st={max(0.0, output_duration - 0.8):.3f}:d=0.8,"
            "loudnorm=I=-16:TP=-1.5:LRA=11[a]"
        )
        audio_map = "[a]"
    elif has_audio:
        graph_parts.append(
            f"[0:a]{_atempo_chain(profile.speed)},"
            "loudnorm=I=-16:TP=-1.5:LRA=11[a]"
        )
        audio_map = "[a]"

    args += ["-filter_complex", ";".join(graph_parts), "-map", "[v]"]
    if audio_map:
        args += ["-map", audio_map]
    else:
        args += ["-an"]
    args += [
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
        "-pix_fmt", "yuv420p", "-r", "30", "-movflags", "+faststart",
    ]
    if audio_map:
        args += ["-c:a", "aac", "-b:a", "160k"]
    args += ["-shortest", str(target)]
    await run_process(*args, timeout=3600)
    return target
