from django.urls import path

from .views import FileUploadView

app_name = "djvue"
urlpatterns = [
    path("file-upload/", view=FileUploadView.as_view(), name="file_upload"),
]
