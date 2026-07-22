from __future__ import annotations

import importlib
import shutil
import sys

MODULES = {
    "aiohttp": "aiohttp",
    "dotenv": "python-dotenv",
    "numpy": "numpy",
    "cv2": "opencv-python-headless",
}
OPTIONAL = {"aiogram": "aiogram", "yt_dlp": "yt-dlp", "scenedetect": "scenedetect"}


def doctor_main() -> int:
    problems: list[str] = []
    print("Python:", sys.version.split()[0])
    if sys.version_info < (3, 11):
        problems.append("Нужен Python 3.11+")
    for module, package in {**MODULES, **OPTIONAL}.items():
        try:
            importlib.import_module(module)
            print("[OK]", package)
        except Exception as exc:
            print("[NO]", package, exc)
            if module in MODULES:
                problems.append(package)
    for command in ("ffmpeg", "ffprobe"):
        path = shutil.which(command)
        print("[OK]" if path else "[NO]", command, path or "")
        if not path:
            problems.append(command)
    print("\nГотово" if not problems else "\nПроблемы: " + ", ".join(problems))
    return 0 if not problems else 1
