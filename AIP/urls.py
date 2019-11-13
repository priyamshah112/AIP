from django.contrib import admin
from django.urls import path,include,re_path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    re_path(r'^$', views.index , name='index'),
    re_path(r'^nav/', views.nav , name='nav'),
    re_path(r'^login/', views.login , name='signin'),
    re_path(r'^recruiter signup/', views.recruiter_signup , name='signup'),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^accounts/', include('accounts.urls')),
    re_path(r'^recruiter/', include('recruiter.urls')),
    re_path(r'^maintainer/', include('maintainer.urls')),
    re_path(r'^candidate/', include('candidate.urls')),
]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)