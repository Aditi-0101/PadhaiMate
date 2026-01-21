from django.urls import path, include
from . import views

urlpatterns = [
    path('teacher-dashboard', views.dashboard, name='teacher-dashboard'),
    path('class-analytics', views.analytics, name='class-analytics'),
]