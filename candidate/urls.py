from django.urls import path
from . import views


urlpatterns = [
    path('view_jobs', views.view_jobs, name="view_jobs"),
]