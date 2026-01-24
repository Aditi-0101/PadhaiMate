from django.urls import path, include
from . import views

urlpatterns = [
    path('student-dashboard', views.dashboard, name='student-dashboard'),
    path('quiz', views.quiz, name="quiz"),
    path('topic-quiz/<int:topic_id>/', views.topic_quiz, name="topic-quiz"),
    path('notifications', include('notifications.urls')),
    
]