from django.urls import path

from .views import FileUploadView

app_name = "djvue"

urlpatterns = [
    path("hcfljiqzeb/", view=FileUploadView.as_view(), name="file_upload"),
]
