from django.urls import path
from . import views

urlpatterns = [
    path('', views.checkImages, name='check-images'),
]