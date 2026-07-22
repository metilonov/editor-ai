from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np

from editai.domain.models import TimeValue


@dataclass(slots=True)
class VisualFeatures:
    motion: list[TimeValue]
    faces: list[TimeValue]
    sharpness: list[TimeValue]
    brightness: list[TimeValue]
    saturation: list[TimeValue]
    entropy: list[TimeValue]


def _entropy(gray: np.ndarray) -> float:
    hist=cv2.calcHist([gray],[0],None,[64],[0,256]).ravel(); total=float(hist.sum())
    if total<=0: return 0.0
    p=hist[hist>0]/total
    return float(-(p*np.log2(p)).sum()/6.0)


def _sync(path: Path, step: float=.75) -> VisualFeatures:
    cap=cv2.VideoCapture(str(path))
    empty=VisualFeatures([],[],[],[],[],[])
    if not cap.isOpened(): return empty
    fps=cap.get(cv2.CAP_PROP_FPS) or 25.0; frames=cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0; duration=frames/fps
    cascade=cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml")
    prev=None; motion=[]; faces=[]; sharp=[]; bright=[]; sat=[]; ent=[]; t=0.0
    while t<=duration:
        cap.set(cv2.CAP_PROP_POS_MSEC,t*1000); ok, frame=cap.read()
        if not ok: break
        small=cv2.resize(frame,(320,180)); gray=cv2.cvtColor(small,cv2.COLOR_BGR2GRAY); hsv=cv2.cvtColor(small,cv2.COLOR_BGR2HSV)
        blur=cv2.GaussianBlur(gray,(5,5),0)
        mv=0.0 if prev is None else float(np.mean(cv2.absdiff(prev,blur))/255.0)
        found=cascade.detectMultiScale(gray,1.2,4,minSize=(24,24)) if not cascade.empty() else []
        motion.append(TimeValue(t,mv)); faces.append(TimeValue(t,min(1.0,len(found)/2.0)))
        sharp.append(TimeValue(t,min(1.0,float(cv2.Laplacian(gray,cv2.CV_64F).var())/1000.0)))
        bright.append(TimeValue(t,float(np.mean(hsv[:,:,2]))/255.0)); sat.append(TimeValue(t,float(np.mean(hsv[:,:,1]))/255.0)); ent.append(TimeValue(t,_entropy(gray)))
        prev=blur; t+=step
    cap.release()
    return VisualFeatures(motion,faces,sharp,bright,sat,ent)


async def analyze_visual(path: Path) -> VisualFeatures:
    return await asyncio.to_thread(_sync,path)
