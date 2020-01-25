from django.urls import path
from . import views


urlpatterns = [
<<<<<<< HEAD
    path('view_jobs', views.view_jobs, name="view_jobs"),
    path('candidate signup', views.candidate_signup, name="candidate_signup"),
    path('jobs_board', views.jobs_board, name="jobs_board"),
    path('edit profile', views.edit_profile, name="edit_profile"), 
    path('applied jobs', views.applied, name="applied jobs"),    
]
=======
    path('jobsboard', views.jobsboard, name="jobsboard"),
    path('profile', views.profile, name="profile"),
    path('resume', views.resume, name="resume"),
    path('applications', views.applications, name="applications"),
    path('job_interview', views.jobInterview, name="jobInterview"),
    path('add_application', views.addApplication, name="addApplication"),
]
>>>>>>> 0e6b95c44511a26dba9a45b68d3f1e230508ae2f
