from __future__ import annotations

import time


class SlidingRateLimit:
    def __init__(self,limit:int=5,window_sec:int=60)->None:self.limit=limit;self.window_sec=window_sec;self.events:dict[int,list[float]]={}
    def allow(self,key:int)->bool:
        now=time.time(); items=[x for x in self.events.get(key,[]) if now-x<self.window_sec]
        if len(items)>=self.limit: self.events[key]=items; return False
        items.append(now); self.events[key]=items; return True
