from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Create your views here.

@login_required
def dashboard(request):
    first_name = request.user.first_name
    last_name = request.user.last_name
    current_date = datetime.now()
    parameters = {
        'first_name': first_name,
        'last_name': last_name,
        'current_date' : current_date,
    }
    return render(request, 'student/student-dashboard.html', parameters)