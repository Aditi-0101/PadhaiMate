from django.urls import path, include
from . import views

urlpatterns = [
    path('kid', views.kid, name='kid'),
]