from django.urls import path
from . import views


urlpatterns = [
    path('login', views.login, name="login"),
    path('recruiter_signup', views.recruiter_signup, name="recruiter_signup"),
    path('candidate_signup', views.candidate_signup, name="candidate_signup"),
]