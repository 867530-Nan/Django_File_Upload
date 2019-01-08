from django.urls import path
from . import views

urlpatterns = [
    path('', views.UploadView.as_view(), name='home_route'),
    path('success/', views.SuccessView.as_view(), name="success"),
    path('failure/', views.FailureView.as_view(), name="failure"),
    path('upload_file/', views.upload_file, name="upload_file_route"),
    path('upload_url/', views.upload_url, name="upload_url_route")
]
