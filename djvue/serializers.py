from tempfile import NamedTemporaryFile

from rest_framework import serializers


class FileUploadSerializer(serializers.Serializer):
    """
    Uploads a file to a temporary directory and returns the file a temporary directory
    and returns the absolute path and original file name
    """

    file = serializers.FileField(required=False, style={"base_template": "file.html"})
    filename = serializers.HiddenField(required=False, default=None)
    path = serializers.HiddenField(required=False, default=None)

    # def validate_file(self, value):
    #     raise serializers.ValidationError("Invalid File format")

    def create(self, validated_data):
        uploaded_file = validated_data["file"]
        with NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(uploaded_file.read())
        return {"path": temp_file.name, "filename": uploaded_file.name}
