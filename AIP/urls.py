from django.contrib import admin
from django.urls import path,include,re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.index , name='index'),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^accounts/', include('accounts.urls')),
    re_path(r'^recruiter/', include('recruiter.urls')),
    re_path(r'^maintainer/', include('maintainer.urls')),
    re_path(r'^candidate/', include('candidate.urls')),
]
