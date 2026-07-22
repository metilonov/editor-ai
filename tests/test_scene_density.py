from editai.analysis.scoring import score_candidate
from editai.domain.models import Candidate,FeatureBundle,Scene
from editai.domain.profiles import get_profile

def test_scene_bonus():
    b=FeatureBundle(scenes=[Scene(0,2),Scene(2,4),Scene(4,6)])
    c=score_candidate(Candidate(0,10),b,get_profile("cinematic"));assert c.features["scenes"]>0
