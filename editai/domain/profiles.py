from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class EditProfile:
    key: str
    title: str
    description: str
    weights: dict[str, float]
    effects: tuple[str, ...] = field(default_factory=tuple)
    speed: float = 1.0
    contrast: float = 1.0
    saturation: float = 1.0
    vignette: bool = False
    transition_sec: float = 0.25


PROFILES: dict[str, EditProfile] = {
    "dynamic": EditProfile("dynamic", "⚡ Dynamic", "Движение, громкость и быстрые сцены", {"motion":.26,"audio":.22,"peaks":.12,"scenes":.15,"faces":.08,"sharpness":.06,"saturation":.05,"entropy":.06}, ("zoom","contrast","flash"), 1.02, 1.08, 1.12),
    "gaming": EditProfile("gaming", "🎮 Gaming", "Экшен, аудиопики и смены сцен", {"motion":.28,"audio":.18,"peaks":.18,"scenes":.16,"faces":.04,"sharpness":.07,"saturation":.05,"entropy":.04}, ("zoom","shake","flash","contrast"), 1.03, 1.10, 1.15),
    "anime": EditProfile("anime", "🌸 Anime", "Контрастные и насыщенные динамичные фрагменты", {"motion":.22,"audio":.16,"peaks":.10,"scenes":.18,"faces":.06,"sharpness":.08,"saturation":.14,"entropy":.06}, ("zoom","contrast","vignette"), 1.0, 1.12, 1.25, True),
    "meme": EditProfile("meme", "😂 Meme", "Лица, аудиопики и короткие реакции", {"motion":.15,"audio":.22,"peaks":.22,"scenes":.10,"faces":.18,"sharpness":.05,"saturation":.03,"entropy":.05}, ("zoom","flash"), 1.0, 1.05, 1.08),
    "cinematic": EditProfile("cinematic", "🎞 Cinematic", "Резкие и визуально насыщенные кадры", {"motion":.12,"audio":.10,"peaks":.06,"scenes":.18,"faces":.08,"sharpness":.16,"saturation":.12,"entropy":.18}, ("contrast","vignette","fade"), .99, 1.12, .92, True, .45),
    "podcast": EditProfile("podcast", "🎙 Podcast", "Лица и активная речь без агрессивных эффектов", {"motion":.08,"audio":.30,"peaks":.12,"scenes":.05,"faces":.30,"sharpness":.08,"saturation":.02,"entropy":.05}, ("clean",), 1.0, 1.02, 1.02),
    "clean": EditProfile("clean", "✨ Clean", "Минимальная обработка", {"motion":.18,"audio":.18,"peaks":.10,"scenes":.15,"faces":.12,"sharpness":.12,"saturation":.05,"entropy":.10}, ("clean",), 1.0, 1.02, 1.03),
    "tiktok": EditProfile("tiktok", "📱 TikTok", "Высокий темп, лица и аудиопики", {"motion":.24,"audio":.20,"peaks":.18,"scenes":.13,"faces":.12,"sharpness":.05,"saturation":.04,"entropy":.04}, ("zoom","flash","contrast"), 1.04, 1.08, 1.12),
}


def get_profile(key: str) -> EditProfile:
    return PROFILES.get(key, PROFILES["dynamic"])
