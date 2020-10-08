from django.core.files.base import ContentFile
from django.core.validators import FileExtensionValidator
from django.urls import reverse_lazy

from rest_framework import serializers

from djvue.fields import FileField, MultipleFileField
from djvue.serializers import FileUploadSerializer
from example.models import Address, Profile, ProfileAttachment


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    # def validate_email(self, value):
    #     raise serializers.ValidationError("Invalid email!")

    def create(self, validated_data):
        return validated_data


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ("name", "country", "zip_code", "address")
        list_serializer_class = serializers.ListSerializer


class WorkSerializer(serializers.Serializer):
    CHOICES = (
        ("cc", "Chocolate Tested"),
        ("dreamer", "Dreamer"),
        ("sp", "Smokes packing"),
    )
    job = serializers.ChoiceField(choices=CHOICES)
    position = serializers.CharField(required=False)

    # def validate_position(self, value):
    #     raise serializers.ValidationError("Invalid Foo")
    #
    # def validate(self, attrs):
    #     raise serializers.ValidationError("Invalid job!")


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=25, min_length=3, required=True,)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(
        write_only=True,
        style={"input_type": "password", "rules": "password:@password2"},
    )
    password2 = serializers.CharField(write_only=True, style={"input_type": "password"})
    multiple_file = MultipleFileField(required=True)
    file = FileField(required=True, style={"upload_url": reverse_lazy("example:pdf_upload")})
    # file = FileField(required=True)
    multiple_file = MultipleFileField(required=True)
    working_place = WorkSerializer(write_only=True)
    # addresses = AddressSerializer(many=True)

    class Meta:
        model = Profile
        fields = (
            "username",
            "email",
            "password1",
            "password2",
            "file",
            "multiple_file",
            "working_place",
        )

    def create(self, validated_data):
        validated_data["password"] = validated_data.pop("password1")
        validated_data.pop("password2")
        validated_data.pop(
            "working_place"
        )  # not required, added only for example purpose
        user_file = validated_data.pop("file", None)
        user_multiple_file = validated_data.pop("multiple_file", None)
        profile = Profile(**validated_data)
        profile.save()
        # # fetch the file from temporary dir
        if user_file is not None and all(
            [user_file.get("path", False), user_file.get("filename", False)]
        ):
            with open(user_file["path"], "rb") as f:
                profile.file.save(user_file["filename"], f)
        if user_multiple_file is not None and all(
            [a_file.get("path", False) and a_file.get("filename", False) for a_file in user_multiple_file]
        ):
            for a_file in user_multiple_file:
                with open(a_file["path"], "rb") as f:
                    ProfileAttachment.objects.create(profile=profile, file=ContentFile(f.read(), a_file["filename"]))
        return profile


class PDFUploadSerializer(FileUploadSerializer):
    """
    Allows only PDF files to be uploaded
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["file"].validators.append(FileExtensionValidator(allowed_extensions=['pdf']))
