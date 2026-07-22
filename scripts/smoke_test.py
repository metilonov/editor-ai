from __future__ import annotations

import asyncio
import shutil
from pathlib import Path

from editai.domain.models import Candidate
from editai.domain.profiles import get_profile
from editai.editing.renderer import render_clip
from editai.media.process import run_process
from editai.media.probe import probe_media


async def main() -> int:
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        print("FFmpeg/ffprobe not found")
        return 1
    root = Path("data/smoke").resolve()
    root.mkdir(parents=True, exist_ok=True)
    source = root / "source.mp4"
    output = root / "result.mp4"
    await run_process(
        "ffmpeg", "-y",
        "-f", "lavfi", "-i", "testsrc2=size=640x360:rate=30:duration=3",
        "-f", "lavfi", "-i", "sine=frequency=440:sample_rate=44100:duration=3",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest",
        str(source), timeout=120,
    )
    await render_clip(
        source, Candidate(0, 2), output, get_profile("dynamic"),
        "blur", None, None, True,
    )
    info = await probe_media(output)
    ok = info.width == 1080 and info.height == 1920 and info.has_audio
    print({"output": str(output), "width": info.width, "height": info.height, "audio": info.has_audio})
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
