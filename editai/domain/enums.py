from enum import StrEnum


class JobStatus(StrEnum):
    QUEUED = "queued"
    DOWNLOADING = "downloading"
    VALIDATING = "validating"
    ANALYZING = "analyzing"
    TRANSCRIBING = "transcribing"
    RENDERING = "rendering"
    SENDING = "sending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class SourceKind(StrEnum):
    URL = "url"
    TELEGRAM_VIDEO = "telegram_video"
    TELEGRAM_DOCUMENT = "telegram_document"
    LOCAL = "local"


class VerticalMode(StrEnum):
    BLUR = "blur"
    CROP = "crop"
    FIT = "fit"
