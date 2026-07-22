from __future__ import annotations

import json
from pathlib import Path

from editai.domain.models import MediaInfo
from editai.media.process import run_process


async def probe_media(path: Path) -> MediaInfo:
    out, _ = await run_process("ffprobe","-v","error","-show_streams","-show_format","-of","json",str(path),timeout=60)
    payload = json.loads(out)
    streams = payload.get("streams", [])
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    if not video: raise RuntimeError("В файле нет видеопотока")
    audio = next((s for s in streams if s.get("codec_type") == "audio"), None)
    rate = str(video.get("avg_frame_rate") or "0/1")
    try:
        n, d = rate.split("/"); fps = float(n) / max(float(d), 1.0)
    except Exception: fps = 0.0
    duration = float(payload.get("format",{}).get("duration") or video.get("duration") or 0)
    return MediaInfo(
        path=path, duration=duration, width=int(video.get("width") or 0), height=int(video.get("height") or 0),
        fps=fps, size_bytes=path.stat().st_size, has_audio=audio is not None,
        video_codec=str(video.get("codec_name") or ""), audio_codec=str((audio or {}).get("codec_name") or ""),
    )
