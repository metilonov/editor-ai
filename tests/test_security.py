from editai.core.security import safe_filename,mask_secret

def test_security():
    assert "/" not in safe_filename("../../a.mp4")
    assert "…" in mask_secret("123456789")
