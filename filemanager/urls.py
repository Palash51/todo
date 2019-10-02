from django.contrib import admin
from django.urls import path

from filemanager import views

app_name = 'fileapp'

urlpatterns = [

    path('v1/signup', views.Signup.as_view(), name='signup'),
    path('v1/signin', views.signin, name='signin'),
    path('v1/signout', views.signout, name='signout'),
    path('v1/todo', views.ToDoListView.as_view(), name='todo'),
    path('v1/generate/url', views.GeneratePublicUrl.as_view(), name='public-url'),
    path('v1/access/todolist', views.AccesslistView.as_view(), name='access-list')

]
