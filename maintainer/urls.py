from django.urls import path
from . import views


urlpatterns = [
    path('mdashboard', views.mdashboard, name="mdashboard"),
    path('users', views.users, name="users"),
    path('post_question',views.post_question,name="post_question"),
    path('post_csv_question',views.post_csv_question,name="post_csv_question"),
    path('edit_question',views.edit_question,name="edit_question"),
    path('delete_question',views.delete_question,name="delete_question"),
]