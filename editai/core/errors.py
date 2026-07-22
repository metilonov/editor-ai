class EditAIError(Exception):
    """Base application error."""


class ConfigurationError(EditAIError):
    pass


class MediaValidationError(EditAIError):
    pass


class DownloadError(EditAIError):
    pass


class RenderError(EditAIError):
    pass


class JobCancelled(EditAIError):
    pass
