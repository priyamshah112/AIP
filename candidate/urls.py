from django.urls import path
from . import views


urlpatterns = [
    path('view_jobs', views.view_jobs, name="view_jobs"),
    path('candidate signup', views.candidate_signup, name="candidate_signup"),
    path('jobs_board', views.jobs_board, name="jobs_board"),
    path('edit profile', views.edit_profile, name="edit_profile"), 
    path('applied jobs', views.applied, name="applied jobs"),    
]