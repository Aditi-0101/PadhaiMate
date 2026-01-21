from django.shortcuts import render

# Create your views here.

def dashboard(request):
    return render(request, 'teacher/teacher-dashboard.html')

def analytics(request):
    return render(request, 'teacher/class-analytics.html')