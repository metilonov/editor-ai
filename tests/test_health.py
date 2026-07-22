from editai.services.health import health_snapshot

def test_health(tmp_path):
    x=health_snapshot(tmp_path);assert "disk_free_gb" in x
