from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def dashboard(request):
    return render(request, 'teacher/teacher-dashboard.html')

@login_required
def analytics(request):
    return render(request, 'teacher/class-analytics.html')