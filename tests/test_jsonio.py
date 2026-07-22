from editai.utils.jsonio import dump_json

def test_json(tmp_path):
    p=dump_json(tmp_path/"x.json",{"а":1});assert "а" in p.read_text(encoding="utf-8")
