from django.urls import path, include
from . import views

urlpatterns = [
    path('student-dashboard', views.dashboard, name='student-dashboard'),
    path('learning-path', views.learning_path, name='learning-path'),
    path('quiz', views.quiz, name="quiz"),
    path('topic-quiz/<int:topic_id>/', views.topic_quiz, name="topic-quiz"),
    path('recommendations', views.recommendations, name='recommendations'),
    path('submit-topic-practice/', views.submit_topic_practice, name="submit-topic-practice"),
    # path('content-recommender/', views.content_recommender, name='content-recommender'),
    path('notifications', include('notifications.urls')),
]