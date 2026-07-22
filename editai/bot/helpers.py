from __future__ import annotations

from editai.core.config import Settings
from editai.domain.models import UserSettings


def default_user_settings(settings:Settings)->UserSettings:
    return UserSettings(settings.default_profile,settings.default_clip_count,settings.default_clip_duration,settings.default_vertical_mode,settings.default_subtitles,settings.default_music)
