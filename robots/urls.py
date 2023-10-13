from django.urls import path
from .views import create_robot, download_robot_summary

urlpatterns = [
    path('create-robot/', create_robot, name='create-robot'),
    path('robot-summary/', download_robot_summary, name='download_robot_summary'),
]