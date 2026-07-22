from __future__ import annotations

from editai.domain.profiles import EditProfile
from editai.editing.effects.registry import effect_filter


def _base_vertical(mode: str, width: int = 1080, height: int = 1920) -> str:
    if mode == "crop":
        return (
            f"scale={width}:{height}:force_original_aspect_ratio=increase,"
            f"crop={width}:{height}"
        )
    if mode == "fit":
        return (
            f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
            f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:black"
        )
    return (
        f"split=2[bg][fg];"
        f"[bg]scale={width}:{height}:force_original_aspect_ratio=increase,"
        f"crop={width}:{height},boxblur=25:5[blur];"
        f"[fg]scale={width}:{height}:force_original_aspect_ratio=decrease[front];"
        f"[blur][front]overlay=(W-w)/2:(H-h)/2"
    )


def build_video_filter(
    mode: str,
    profile: EditProfile,
    duration: float,
    subtitles_path: str | None = None,
) -> str:
    filters = [_base_vertical(mode)]
    output_duration = duration / max(profile.speed, 0.01)
    values = {
        "contrast": profile.contrast,
        "saturation": profile.saturation,
        "transition": profile.transition_sec,
        "fade_out": max(0.0, output_duration - profile.transition_sec),
    }
    for key in profile.effects:
        current = effect_filter(key, **values)
        if current:
            filters.append(current)
    if abs(profile.speed - 1.0) > 1e-3:
        filters.append(f"setpts=PTS/{profile.speed:.4f}")
    if subtitles_path:
        escaped = subtitles_path.replace("\\", "/").replace(":", "\\:").replace("'", "\\'")
        filters.append(
            f"subtitles='{escaped}':"
            "force_style='Alignment=2,FontSize=18,Outline=3,Shadow=1,MarginV=110'"
        )
    return ",".join(filters)
