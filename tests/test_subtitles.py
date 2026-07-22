from editai.domain.models import SubtitleSegment
from editai.editing.subtitles import write_clip_srt

def test_subtitles(tmp_path):
    p=write_clip_srt([SubtitleSegment(5,8,"Привет")],4,10,tmp_path/"x.srt")
    assert p and "Привет" in p.read_text(encoding="utf-8")
