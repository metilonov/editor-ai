from __future__ import annotations

from editai.analysis.sampling import window_mean
from editai.domain.models import Candidate, FeatureBundle
from editai.domain.profiles import EditProfile
from editai.utils.math import clamp


def _scene_density(bundle: FeatureBundle,start:float,end:float)->float:
    cuts=sum(1 for s in bundle.scenes if start<=s.start<end)
    return clamp(cuts/max(1.0,(end-start)/5.0))


def score_candidate(candidate: Candidate,bundle: FeatureBundle,profile:EditProfile)->Candidate:
    f={
        "motion":window_mean(bundle.motion,candidate.start,candidate.end),
        "audio":window_mean(bundle.audio_rms,candidate.start,candidate.end),
        "peaks":window_mean(bundle.audio_peaks,candidate.start,candidate.end),
        "scenes":_scene_density(bundle,candidate.start,candidate.end),
        "faces":window_mean(bundle.faces,candidate.start,candidate.end),
        "sharpness":window_mean(bundle.sharpness,candidate.start,candidate.end),
        "brightness":window_mean(bundle.brightness,candidate.start,candidate.end),
        "saturation":window_mean(bundle.saturation,candidate.start,candidate.end),
        "entropy":window_mean(bundle.entropy,candidate.start,candidate.end),
    }
    weighted=sum(profile.weights.get(k,0.0)*clamp(v) for k,v in f.items())
    reasons=[]
    labels={"motion":"много движения","audio":"активный звук","peaks":"аудиопики","scenes":"частые смены сцен","faces":"лица в кадре","sharpness":"четкая картинка","saturation":"насыщенные цвета","entropy":"визуальная детализация"}
    for key in sorted(profile.weights,key=lambda x:f.get(x,0)*profile.weights.get(x,0),reverse=True)[:3]:
        if f.get(key,0)>.25: reasons.append(labels.get(key,key))
    if f["audio"]<.03 and profile.key not in {"cinematic","clean"}: weighted*=.82
    if f["sharpness"]<.12: weighted*=.8
    candidate.features=f; candidate.score=clamp(weighted); candidate.reasons=reasons
    return candidate


def score_all(candidates:list[Candidate],bundle:FeatureBundle,profile:EditProfile)->list[Candidate]:
    return [score_candidate(c,bundle,profile) for c in candidates]
