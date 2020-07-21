# -*- coding: utf-8 -*-
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from django.conf import settings

from rest_framework import serializers


class FileUploadSerializer(serializers.Serializer):
    """
    Uploads a file to a temporary directory and
    returns the absolute path and original file name
    """

    file = serializers.FileField(style={"base_template": "file.html"}, required=False)

    def create(self, validated_data):
        uploaded_file = validated_data["file"]
        path = os.path.join(settings.MEDIA_ROOT, "tmp/uploaded_files")
        Path(path).mkdir(parents=True, exist_ok=True)
        with NamedTemporaryFile(delete=False, dir=path) as temp_file:
            temp_file.write(uploaded_file.read())
        return {"path": temp_file.name, "filename": uploaded_file.name}
