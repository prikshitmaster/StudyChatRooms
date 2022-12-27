from django.contrib import admin
from django.urls import path

from base import views

urlpatterns = [

    path('', views.home, name='home'),
    path('room/<str:pk>/', views.room, name='room'),
    path('createroom', views.createroom, name='createroom'),
    path('createtopic', views.createtopic, name='createtopic'),
    path('update-room/<str:pk>/', views.updateroom, name='update-room'),
    path('delete-room/<str:pk>/', views.deleteroom, name='delete-room'),
    path('delete-room/<str:pk>/', views.deleteroom, name='delete-room'),
    path('deletemessage/<str:pk>/', views.deletemessage, name='deletemessage'),
    path('userProfile/<str:pk>/', views.userProfile, name='userProfile'),
    path('register/', views.register, name='register'),

]
