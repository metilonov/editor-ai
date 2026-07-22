from editai.analysis.candidates import generate_candidates
from editai.domain.models import FeatureBundle,Scene,TimeValue

def test_candidates():
    b=FeatureBundle(scenes=[Scene(10,20)],audio_peaks=[TimeValue(40,1)])
    x=generate_candidates(120,b,30,10)
    assert len(x)>3
    assert all(c.duration>=10 for c in x)
