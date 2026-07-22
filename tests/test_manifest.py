from editai.domain.models import Candidate,MediaInfo,UserSettings
from editai.editing.manifest import write_manifest

def test_manifest(tmp_path):
    src=tmp_path/"a.mp4";src.write_bytes(b"x")
    info=MediaInfo(src,10,100,100,25,1,False)
    p=write_manifest(tmp_path/"m.json",info,UserSettings(),[(Candidate(0,5),tmp_path/"c.mp4")])
    assert '"clips"' in p.read_text()
