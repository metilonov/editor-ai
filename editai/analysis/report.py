from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from editai.domain.models import Candidate, FeatureBundle, MediaInfo
from editai.utils.jsonio import dump_json


def write_report(path:Path,info:MediaInfo,bundle:FeatureBundle,candidates:list[Candidate],selected:list[Candidate],profile:str)->Path:
    payload={"media":asdict(info),"profile":profile,"feature_counts":{k:len(v) for k,v in asdict(bundle).items()},"candidates":candidates,"selected":selected}
    return dump_json(path,payload)
