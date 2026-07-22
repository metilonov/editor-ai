from editai.analysis.scoring import score_candidate
from editai.domain.models import Candidate,FeatureBundle,TimeValue
from editai.domain.profiles import get_profile

def test_scoring():
    series=[TimeValue(i,1.0) for i in range(30)]
    b=FeatureBundle(motion=series,audio_rms=series,audio_peaks=series,faces=series,sharpness=series,saturation=series,entropy=series)
    c=score_candidate(Candidate(0,30),b,get_profile("dynamic"))
    assert c.score>.5
    assert c.reasons
