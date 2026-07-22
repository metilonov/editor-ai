from __future__ import annotations

import asyncio
from pathlib import Path

import cv2
import numpy as np

from editai.domain.models import Scene


def _fallback(path: Path, threshold: float = .38, step: float = .5) -> list[Scene]:
    cap = cv2.VideoCapture(str(path)); result: list[Scene] = []
    if not cap.isOpened(): return result
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0; frames = cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0; duration = frames/fps
    previous = None; cuts=[0.0]; t=0.0
    while t < duration:
        cap.set(cv2.CAP_PROP_POS_MSEC,t*1000); ok, frame=cap.read()
        if not ok: break
        hsv=cv2.cvtColor(cv2.resize(frame,(160,90)),cv2.COLOR_BGR2HSV)
        hist=cv2.calcHist([hsv],[0,1],None,[24,24],[0,180,0,256]); cv2.normalize(hist,hist)
        if previous is not None:
            dist=float(cv2.compareHist(previous,hist,cv2.HISTCMP_BHATTACHARYYA))
            if dist>=threshold and t-cuts[-1]>=1.0: cuts.append(t)
        previous=hist; t+=step
    cap.release(); cuts.append(duration)
    for a,b in zip(cuts,cuts[1:]):
        if b-a>=.3: result.append(Scene(a,b,1.0))
    return result


def _sync(path: Path) -> list[Scene]:
    try:
        from scenedetect import ContentDetector, detect
        pairs=detect(str(path),ContentDetector(threshold=27.0),show_progress=False)
        scenes=[Scene(a.get_seconds(),b.get_seconds(),1.0) for a,b in pairs]
        return scenes or _fallback(path)
    except Exception:
        return _fallback(path)


async def detect_scenes(path: Path) -> list[Scene]:
    return await asyncio.to_thread(_sync,path)
