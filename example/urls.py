# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.urls import path, include
from .views import LoginView, ProfileView, PDFUploadView

app_name = "example"

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('pdf-upload/', PDFUploadView.as_view(), name="pdf_upload")
]
