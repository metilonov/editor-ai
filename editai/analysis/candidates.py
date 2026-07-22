from __future__ import annotations

from editai.domain.models import Candidate, FeatureBundle


def generate_candidates(duration: float, features: FeatureBundle, clip_duration: float, min_duration: float=10.0) -> list[Candidate]:
    window=min(clip_duration,duration); candidates: list[Candidate]=[]
    anchors={0.0,max(0.0,duration-window)}
    stride=max(4.0,window/3)
    t=0.0
    while t<duration: anchors.add(max(0.0,min(t,duration-window))); t+=stride
    for scene in features.scenes:
        anchors.add(max(0.0,min(scene.start-1.0,duration-window)))
        anchors.add(max(0.0,min((scene.start+scene.end-window)/2,duration-window)))
    for item in features.audio_peaks:
        anchors.add(max(0.0,min(item.time-window*.35,duration-window)))
    for start in sorted(anchors):
        end=min(duration,start+window)
        if end-start>=min_duration: candidates.append(Candidate(start,end))
    unique={(round(c.start,2),round(c.end,2)):c for c in candidates}
    return list(unique.values())
