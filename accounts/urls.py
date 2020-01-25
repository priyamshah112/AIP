from django.urls import path, include, re_path
from . import views

app_name = 'accounts'
urlpatterns = [
    re_path(r'^login', views.login, name='login'),
    re_path(r'^recruiter_signup', views.recruiter_signup, name='recruiter_signup'),
    re_path(r'^candidate_signup', views.candidate_signup, name='candidate_signup'),    
    re_path(r'^logout', views.logout, name='logout'),
]