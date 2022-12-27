from django.contrib import admin
from django.urls import path

from base import views

urlpatterns = [

    path('login', views.loginpage, name='loginpage'),
    path('logout', views.logoutpage, name='logoutpage')

]
