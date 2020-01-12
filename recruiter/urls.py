from django.urls import path
from . import views


urlpatterns = [

    path('jobs', views.jobs, name="jobs"),
    path('candidates', views.candidates, name="candidates"),
    path('question', views.question, name="question"),
    path('deletepost',views.deletepost,name="deletepost"),
    path('addpackage', views.addpackage, name="addpackage"),
    path('loadquestions', views.loadquestions, name="loadquestions"),
    path('addquestion', views.addquestion, name="addquestion"),
    path('deletequestion', views.deletequestion, name="deletequestion"),
    path('getPackages', views.getPackages, name="getPackages"),
    path('changepackage', views.changepackage, name="changepackage"),
    path('view_interview/<jid>/<candidate_id>/', views.view_interview, name="view_interview"),
    path('view_interview', views.view_interview, name="view_interview"),
    path('hiremail', views.hiremail, name="hiremail"),
    path('rejmail', views.rejmail, name="rejmail"),
]