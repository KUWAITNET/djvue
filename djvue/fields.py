from rest_framework.fields import DictField
from rest_framework.settings import api_settings

from .validators import RequiredFileValidator


class FileField(DictField):
    """
    A hybrid file field. Renders an input type,
    accepts as input a dictionary containing the filename and the file path
    and it serializes the representation like a native serializer.FileField
    """

    default_validators = [RequiredFileValidator()]

    def __init__(self, **kwargs):
        kwargs["style"] = kwargs.get("style", {})
        if "base_template" not in kwargs["style"]:
            kwargs["style"]["base_template"] = "file.html"
        super().__init__(**kwargs)

    def to_representation(self, value):
        if not value:
            return None

        use_url = getattr(self, "use_url", api_settings.UPLOADED_FILES_USE_URL)
        if use_url:
            try:
                url = value.url
            except AttributeError:
                return None
            request = self.context.get("request", None)
            if request is not None:
                return request.build_absolute_uri(url)
            return url

        return value.name
