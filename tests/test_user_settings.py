from editai.domain.models import UserSettings

def test_user_settings():
    s=UserSettings();assert s.to_dict()["profile"]=="dynamic"
