from __future__ import annotations

import shutil
from pathlib import Path


def health_snapshot(data_dir:Path)->dict[str,object]:
    usage=shutil.disk_usage(data_dir)
    return {"ffmpeg":bool(shutil.which("ffmpeg")),"ffprobe":bool(shutil.which("ffprobe")),"disk_free_gb":round(usage.free/1024**3,2),"data_dir":str(data_dir)}
