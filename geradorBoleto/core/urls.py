from django.urls import path

from . import views


urlpatterns = [
    path("upload-csv/", views.UploadCSVView.as_view(), name="upload_csv_file"),
]
