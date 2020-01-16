from django.urls import path
from . import views


urlpatterns = [
    path('jobsboard', views.jobsboard, name="jobsboard"),
    path('profile', views.profile, name="profile"),
    path('resume', views.resume, name="resume"),
    path('applications', views.applications, name="applications"),
    path('saved_applications',views.saved,name='saved_applications'),
    path('job_interview', views.jobInterview, name="jobInterview"),
    path('add_application', views.addApplication, name="addApplication"),
    path('introduction', views.introduction, name="introduction"),
    # path('save_mcq', views.save_mcq, name="save_mcq"),
    path('new_application', views.new_application, name='new_application'),
    path('resume_upload', views.resume_upload, name='Resume_upload'),
]