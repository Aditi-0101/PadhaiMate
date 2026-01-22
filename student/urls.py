from django.urls import path, include
from . import views

urlpatterns = [
    path('student-dashboard', views.dashboard, name='student-dashboard'),
    path('quiz', views.quiz, name="quiz"),
    path('notifications', include('notifications.urls')),
    
]