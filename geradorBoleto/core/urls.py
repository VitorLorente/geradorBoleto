from django.urls import path

from . import views


urlpatterns = [
    path("upload_csv/", views.UploadCSVView.as_view(), name="upload_csv_file"),
    path("get_task_status/", views.get_task_status, name="get_task_status"),
]
