from django.urls import path
from .views import create_robot

urlpatterns = [
    path('create-robot/', create_robot, name='create-robot'),
]