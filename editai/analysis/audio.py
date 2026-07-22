from __future__ import annotations

import asyncio
import wave
from pathlib import Path

import numpy as np

from editai.domain.models import TimeValue
from editai.media.ffmpeg import extract_audio


def _sync(path: Path, window_sec: float=.5) -> tuple[list[TimeValue],list[TimeValue]]:
    with wave.open(str(path),"rb") as wav:
        channels=wav.getnchannels(); rate=wav.getframerate(); width=wav.getsampwidth()
        if width!=2: return [],[]
        size=max(1,int(rate*window_sec)); rms=[]; zcr=[]; i=0
        while True:
            raw=wav.readframes(size)
            if not raw: break
            data=np.frombuffer(raw,dtype=np.int16).astype(np.float32)
            if channels>1: data=data.reshape(-1,channels).mean(axis=1)
            value=float(np.sqrt(np.mean(np.square(data)))/32768.0) if data.size else 0.0
            crossings=float(np.mean(np.abs(np.diff(np.signbit(data))))) if data.size>1 else 0.0
            rms.append(TimeValue(i*window_sec,value)); zcr.append(TimeValue(i*window_sec,crossings)); i+=1
    if not rms: return rms,[]
    vals=np.array([x.value for x in rms]); threshold=float(np.quantile(vals,.88)) if len(vals)>3 else float(vals.max())
    peaks=[TimeValue(x.time, min(1.0,x.value/max(threshold,1e-9))) for x in rms if x.value>=threshold]
    return rms,peaks


async def analyze_audio(source: Path, work_dir: Path, has_audio: bool) -> tuple[list[TimeValue],list[TimeValue],Path|None]:
    if not has_audio: return [],[],None
    wav=work_dir/"audio.wav"
    try:
        await extract_audio(source,wav)
        rms,peaks=await asyncio.to_thread(_sync,wav)
        return rms,peaks,wav
    except Exception:
        return [],[],None
