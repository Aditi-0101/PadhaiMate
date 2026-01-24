from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Question
from .models import StudentProfile
from student.utils.level_helper import get_level_for_questions

# Create your views here.

@login_required
def dashboard(request):
    if request.session.get("clear_answers"):
        request.session.pop("answers", None)
        request.session.pop("clear_answers", None)

    first_name = request.user.first_name
    last_name = request.user.last_name
    current_date = datetime.now()

    test_result = request.session.get("last_test_result")
    overall_level = request.session.get("overall_level")

    student_profile = request.user.student_profile
    maths_level = student_profile.maths_level
    science_level = student_profile.science_level
    english_level = student_profile.english_level

    parameters = {
        'first_name': first_name,
        'last_name': last_name,
        'current_date': current_date,
        'test_result': test_result,
        'overall_level': overall_level,
        'maths_level': maths_level,
        'science_level': science_level,
        'english_level': english_level,
    }

    return render(request, 'student/student-dashboard.html', parameters)

@login_required
def quiz(request):
    student_profile = StudentProfile.objects.get(user=request.user)
    class_level = student_profile.student_class
    
    maths_qs = list(
        Question.objects.filter(
            class_level=class_level,
            subject_name="Maths"
            )[:7]
    )
    science_qs = list(
        Question.objects.filter(
            class_level=class_level,
            subject_name="Science"
            )[:7]
    )    
    english_qs = list(
        Question.objects.filter(
            class_level=class_level,
            subject_name="English"
            )[:6]
    )
    all_questions = maths_qs + science_qs + english_qs
    if not all_questions:
        return render(request, "student/quiz.html", {
        "error": "No questions available for your class"
    })        
    current_index = int(request.POST.get("current_index", 1)) if request.method == "POST" else 1
        
    if "answers" not in request.session:
        request.session["answers"] = {}

    if request.method == "POST":
        action = request.POST.get("action")
        current_index = int(request.POST.get("current_index", 1))
        selected_answer = request.POST.get("answer")
        question_id = request.POST.get("question_id")

        if selected_answer and question_id:
            request.session["answers"][question_id] = selected_answer
            request.session.modified = True         

        if action == "next":
            current_index += 1

        elif action == "prev":
            current_index -= 1 
            
        elif action == "finish":
            if selected_answer and question_id:
                request.session["answers"][question_id] = selected_answer
                request.session.modified = True            
            answers = request.session.get("answers", {})
            score = 0            
            ########################################### CALCULATE SCORE #######################################################
            for q in all_questions:
                if str(q.id) in answers and answers[str(q.id)] == q.correct_option:
                    score += 1
            ######################################### LEVEL(BASED ON TOTAL SCORE) ###############################################
            if score <= 5:
                overall_level = "Beginner"
            elif score <= 10:
                overall_level = "Intermediate"
            else:
                overall_level = "Advanced"           
            request.session["overall_level"] = overall_level
            request.session.modified = True

            ########################################### SUBJECT-WISE LEVELS #####################################################
            maths_level = get_level_for_questions(maths_qs, answers)
            science_level = get_level_for_questions(science_qs, answers)
            english_level = get_level_for_questions(english_qs, answers)
            
            student_profile.maths_level = maths_level
            student_profile.science_level = science_level
            student_profile.english_level = english_level
            student_profile.save()
            
            print("Maths Level:", maths_level)
            print("Science Level:", science_level)
            print("English Level:", english_level)

            request.session["last_test_result"] = {
                "attempted": len(answers),
                "score": int(score),
                "total": int(len(all_questions)),
            }
            request.session.modified = True
            request.session["clear_answers"] = True
            return redirect("student-dashboard")
    else:
        current_index = 1            
    if current_index < 1:
        current_index = 1
    if current_index > len(all_questions):
        current_index = len(all_questions)        
    current_question = all_questions[current_index - 1]
    current_subject = current_question.subject_name
    saved_answer = request.session.get("answers", {}).get(str(current_question.id))

    context = {
        "question": current_question,
        "current_index": current_index,
        "total_questions": len(all_questions),

        "maths_range": range(1, 8),
        "science_range": range(1, 8),
        "english_range": range(1, 7),

        "current_subject": current_subject,
        "saved_answer": saved_answer,
        
        "answers": request.session.get("answers", {}),
        "all_questions": all_questions,
        "current_question_id": str(current_question.id),
    }

    return render(request, "student/quiz.html", context)
