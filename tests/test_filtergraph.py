from editai.domain.profiles import get_profile
from editai.editing.filtergraph import build_video_filter

def test_filtergraph():
    x=build_video_filter("blur",get_profile("dynamic"),30,None)
    assert "overlay" in x and "eq=" in x
