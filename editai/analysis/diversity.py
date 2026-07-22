from __future__ import annotations

from editai.domain.models import Candidate
from editai.utils.math import overlap_ratio


def select_diverse(candidates:list[Candidate],count:int,max_overlap:float=.2,min_gap:float=1.0)->list[Candidate]:
    selected=[]
    for item in sorted(candidates,key=lambda c:c.score,reverse=True):
        if any(overlap_ratio(item.start,item.end,x.start,x.end)>max_overlap or abs(item.start-x.end)<min_gap or abs(x.start-item.end)<min_gap for x in selected):
            continue
        selected.append(item)
        if len(selected)>=count: break
    if not selected and candidates: selected=[max(candidates,key=lambda c:c.score)]
    return sorted(selected,key=lambda c:c.start)
