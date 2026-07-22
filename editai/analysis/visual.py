from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import cv2
import numpy as np

from editai.domain.models import TimeValue


@dataclass(slots=True)
class VisualFeatures:
    motion: list[TimeValue]
    faces: list[TimeValue]
    sharpness: list[TimeValue]
    brightness: list[TimeValue]
    saturation: list[TimeValue]
    entropy: list[TimeValue]


def _empty_features() -> VisualFeatures:
    return VisualFeatures(
        motion=[],
        faces=[],
        sharpness=[],
        brightness=[],
        saturation=[],
        entropy=[],
    )


def _opencv_has_basic_video_support() -> bool:
    required_attributes = (
        "VideoCapture",
        "CAP_PROP_FPS",
        "CAP_PROP_FRAME_COUNT",
        "CAP_PROP_POS_MSEC",
        "resize",
        "cvtColor",
        "COLOR_BGR2GRAY",
        "COLOR_BGR2HSV",
        "GaussianBlur",
        "absdiff",
        "Laplacian",
        "CV_64F",
    )

    return all(
        hasattr(cv2, attribute)
        for attribute in required_attributes
    )


def _entropy(gray: np.ndarray) -> float:
    if not hasattr(cv2, "calcHist"):
        return 0.0

    try:
        histogram = cv2.calcHist(
            [gray],
            [0],
            None,
            [64],
            [0, 256],
        ).ravel()
    except Exception:
        return 0.0

    total = float(histogram.sum())

    if total <= 0:
        return 0.0

    probabilities = histogram[histogram > 0] / total

    return float(
        -(probabilities * np.log2(probabilities)).sum() / 6.0
    )


def _create_face_detector() -> Any | None:
    classifier = getattr(
        cv2,
        "CascadeClassifier",
        None,
    )

    cv2_data = getattr(
        cv2,
        "data",
        None,
    )

    haarcascades = getattr(
        cv2_data,
        "haarcascades",
        None,
    )

    if classifier is None or not haarcascades:
        return None

    cascade_path = (
        Path(haarcascades)
        / "haarcascade_frontalface_default.xml"
    )

    if not cascade_path.exists():
        return None

    try:
        detector = classifier(str(cascade_path))

        if hasattr(detector, "empty") and detector.empty():
            return None

        return detector
    except Exception:
        return None


def _detect_faces(
    detector: Any | None,
    gray: np.ndarray,
) -> float:
    if detector is None:
        return 0.0

    try:
        faces = detector.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=4,
            minSize=(24, 24),
        )
    except Exception:
        return 0.0

    return min(
        1.0,
        len(faces) / 2.0,
    )


def _sync(
    path: Path,
    step: float = 0.75,
) -> VisualFeatures:
    if not _opencv_has_basic_video_support():
        return _empty_features()

    capture = cv2.VideoCapture(str(path))

    if not capture.isOpened():
        capture.release()
        return _empty_features()

    motion: list[TimeValue] = []
    faces: list[TimeValue] = []
    sharpness: list[TimeValue] = []
    brightness: list[TimeValue] = []
    saturation: list[TimeValue] = []
    entropy: list[TimeValue] = []

    try:
        fps = float(
            capture.get(cv2.CAP_PROP_FPS)
            or 25.0
        )

        frame_count = float(
            capture.get(cv2.CAP_PROP_FRAME_COUNT)
            or 0.0
        )

        duration = (
            frame_count / fps
            if fps > 0
            else 0.0
        )

        detector = _create_face_detector()
        previous_blurred: np.ndarray | None = None
        timestamp = 0.0
        sample_step = max(float(step), 0.1)

        while timestamp <= duration:
            capture.set(
                cv2.CAP_PROP_POS_MSEC,
                timestamp * 1000.0,
            )

            success, frame = capture.read()

            if not success or frame is None:
                break

            try:
                small = cv2.resize(
                    frame,
                    (320, 180),
                )

                gray = cv2.cvtColor(
                    small,
                    cv2.COLOR_BGR2GRAY,
                )

                hsv = cv2.cvtColor(
                    small,
                    cv2.COLOR_BGR2HSV,
                )

                blurred = cv2.GaussianBlur(
                    gray,
                    (5, 5),
                    0,
                )
            except Exception:
                timestamp += sample_step
                continue

            motion_value = 0.0

            if previous_blurred is not None:
                try:
                    difference = cv2.absdiff(
                        previous_blurred,
                        blurred,
                    )

                    motion_value = float(
                        np.mean(difference) / 255.0
                    )
                except Exception:
                    motion_value = 0.0

            face_value = _detect_faces(
                detector,
                gray,
            )

            try:
                sharpness_value = min(
                    1.0,
                    float(
                        cv2.Laplacian(
                            gray,
                            cv2.CV_64F,
                        ).var()
                    )
                    / 1000.0,
                )
            except Exception:
                sharpness_value = 0.0

            try:
                brightness_value = float(
                    np.mean(hsv[:, :, 2])
                ) / 255.0
            except Exception:
                brightness_value = 0.0

            try:
                saturation_value = float(
                    np.mean(hsv[:, :, 1])
                ) / 255.0
            except Exception:
                saturation_value = 0.0

            entropy_value = _entropy(gray)

            motion.append(
                TimeValue(
                    timestamp,
                    motion_value,
                )
            )

            faces.append(
                TimeValue(
                    timestamp,
                    face_value,
                )
            )

            sharpness.append(
                TimeValue(
                    timestamp,
                    sharpness_value,
                )
            )

            brightness.append(
                TimeValue(
                    timestamp,
                    brightness_value,
                )
            )

            saturation.append(
                TimeValue(
                    timestamp,
                    saturation_value,
                )
            )

            entropy.append(
                TimeValue(
                    timestamp,
                    entropy_value,
                )
            )

            previous_blurred = blurred
            timestamp += sample_step

    finally:
        capture.release()

    return VisualFeatures(
        motion=motion,
        faces=faces,
        sharpness=sharpness,
        brightness=brightness,
        saturation=saturation,
        entropy=entropy,
    )


async def analyze_visual(
    path: Path,
) -> VisualFeatures:
    try:
        return await asyncio.to_thread(
            _sync,
            path,
        )
    except Exception:
        return _empty_features()
