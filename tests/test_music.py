from editai.editing.music import choose_music

def test_music(tmp_path):
    assert choose_music(tmp_path,"x") is None
    (tmp_path/"a.mp3").write_bytes(b"x");assert choose_music(tmp_path,"x").name=="a.mp3"
