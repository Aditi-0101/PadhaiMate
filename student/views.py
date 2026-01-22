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

def quiz(request):
    if request.method == "GET":
        class_level = request.GET.get("class_level")
        subject_name = request.GET.get("subject_name")
        difficulty = request.GET.get("difficulty")
        question_text = request.GET.get("question_text")
        option_a = request.GET.get("option_a")
        option_b = request.GET.get("option_b")
        option_c = request.GET.get("option_c")
        option_d = request.GET.get("option_d")
        context = {
            "class_level": class_level,
            "subject_name": subject_name,
            "difficulty": difficulty,
            "question_text": question_text,
            "option_a": option_a,
            "option_b": option_b,
            "option_c": option_c,
            "option_d": option_d,
        }
    return render(request, 'student/quiz.html', context)