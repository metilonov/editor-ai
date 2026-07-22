from editai.domain.profiles import PROFILES,get_profile

def test_profiles():
    assert len(PROFILES)>=8
    assert get_profile("missing").key=="dynamic"
    assert abs(sum(PROFILES["dynamic"].weights.values())-1)<1e-6
