from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('student/', include('student.urls')),
    path('teacher/', include('teacher.urls')),
    path('kid/', include('kid.urls')),
]