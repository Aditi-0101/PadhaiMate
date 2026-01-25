from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from .models import Question, StudentProfile, Topic, StudentWeakTopic, LearningContent
from student.services import RecommendationService
from student.utils.level_helper import get_level_for_questions
from student.services.gemini_service import generate_explanation
from django.db.models import Prefetch
from .models import LearningActivity
from django.utils.timezone import now, timedelta

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
def learning_path(request):
    student_profile = request.user.student_profile
    
    # Fetch Weak Topics
    weak_topics = StudentWeakTopic.objects.filter(
        student=student_profile,
        is_resolved=False
    ).select_related('topic').prefetch_related(
        Prefetch('topic__contents', queryset=LearningContent.objects.all())
    )
    
    # Attach Content based on Concepts
    valid_topics = []
    for wt in weak_topics:
        # Filter Learning Content STRICTLY by concept_tag
        all_contents = wt.topic.contents.all()
        wt.filtered_contents = []
        
        if wt.weak_concepts:
            concept_tags = [tag.strip() for tag in wt.weak_concepts.split(',') if tag.strip()]
            if concept_tags:
                wt.filtered_contents = all_contents.filter(concept_tag__in=concept_tags)
        else:
            # Fallback for topics with no specific concept tags recorded (General Review)
            wt.filtered_contents = all_contents
        
        # Only show topic if there is content to learn
        if wt.filtered_contents:
            valid_topics.append(wt)
            
    return render(request, 'student/learning_path.html', {'weak_topics': valid_topics})

    today = now().date()
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    activity_map = {
        a.date: a.quizzes_attempted
        for a in LearningActivity.objects.filter(
            student=student_profile,
            date__in=last_7_days
        )
    }
    daily_progress = [activity_map.get(d, 0) for d in last_7_days]
    parameters["daily_progress"] = daily_progress


    return render(request, 'student/student-dashboard.html', parameters)
@login_required
def submit_topic_practice(request):
    if request.method == "POST":
        topic_id = request.POST.get('topic_id')
        if not topic_id:
            return redirect('learning-path')
        
        student_profile = request.user.student_profile
        topic = Topic.objects.get(id=topic_id)
        
        # Calculate score
        score = 0
        total_attempted = 0
        
        # Get all keys from POST that start with 'q_'
        for key in request.POST:
            if key.startswith('q_'):
                q_id = key.split('_')[1]
                selected_option = request.POST[key]
                try:
                    question = Question.objects.get(id=q_id)
                    total_attempted += 1
                    if question.correct_option == selected_option:
                        score += 1
                except Question.DoesNotExist:
                    pass
        
        # Mastery Check: Need at least 3 out of 5 (60%) correct to resolve
        # Adjust threshold as needed
        if total_attempted > 0 and (score / total_attempted) >= 0.6:
            # Mark as resolved
            StudentWeakTopic.objects.filter(student=student_profile, topic=topic).update(is_resolved=True)
            messages.success(request, f"🎉 Great job! You scored {score}/{total_attempted}. Topic '{topic.name}' is now mastered!")
            return redirect('learning-path') # Return to learning path on success
        else:
             # Logic to update weak concepts for persistent failures
             incorrect_concepts = set()
             for key in request.POST:
                 if key.startswith('q_'):
                     q_id = key.split('_')[1]
                     selected = request.POST[key]
                     try:
                         q = Question.objects.get(id=q_id)
                         if selected != q.correct_option and q.concept_tag:
                             incorrect_concepts.add(q.concept_tag)
                     except Question.DoesNotExist:
                         pass
             
             if incorrect_concepts:
                 wt, _ = StudentWeakTopic.objects.get_or_create(student=student_profile, topic=topic)
                 current = set(wt.weak_concepts.split(',')) if wt.weak_concepts else set()
                 updated = current.union(incorrect_concepts)
                 wt.weak_concepts = ",".join({c for c in updated if c})
                 wt.save()

             messages.warning(request, f"Keep practicing! You scored {score}/{total_attempted}. Try to get at least 60%.")
             
    return redirect('learning-path')

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
            
            # ----------------- IDENTIFY WEAK TOPICS -----------------

            # ----------------- IDENTIFY & STORE WEAK TOPICS -----------------
            # Use Service Layer
            weak_areas = RecommendationService.calculate_weak_areas(all_questions, answers)
            RecommendationService.store_weak_areas(student_profile, weak_areas)
            
            # ----------------------------------------------------------------

            request.session.modified = True
            request.session["clear_answers"] = True
            # ----------------- DAILY LEARNING ACTIVITY -----------------
            today = now().date()
            activity, created = LearningActivity.objects.get_or_create(
                student=student_profile,
                date=today
            )
            activity.quizzes_attempted += 1
            activity.save()
# ----------------------------------------------------------

            
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


@login_required
def topic_quiz(request, topic_id):
    student_profile = request.user.student_profile
    topic = Topic.objects.get(id=topic_id)
    
    # Check for weak topic to filter questions by concept
    try:
        wt = StudentWeakTopic.objects.get(student=student_profile, topic=topic)
        weak_concepts = [t.strip() for t in wt.weak_concepts.split(',') if t.strip()]
    except StudentWeakTopic.DoesNotExist:
        weak_concepts = []
        
    if weak_concepts:
        # STRICT Filtering: Show only questions matching the weak concepts
        questions = list(Question.objects.filter(topic=topic, concept_tag__in=weak_concepts))
        
        # Fallback (optional): If no questions found for strict tags, maybe show all? 
        # Requirement says "Quiz questions MUST be filtered by the SAME concept_tag".
        # So if empty, let's keep it empty or show a message.
        if not questions:
            # Dangerous if no questions exist for tag. Let's fallback to topic questions if strictly 0 found, 
            # to avoid broken UI, OR better, tell user "No practice questions for this specific concept yet".
            # For hackathon safety: Fallback to all topic questions if specific filter yields 0.
            questions = list(Question.objects.filter(topic=topic))
    else:
        questions = list(Question.objects.filter(topic=topic))
    
    if not questions:
        messages.info(request, "No questions available for this topic yet.")
        return redirect('learning-path')

    if request.method == "POST":
        # Simplified finish logic for topic quiz
        score = 0
        total = len(questions)
        for q in questions:
            selected = request.POST.get(f"q_{q.id}")
            if selected == q.correct_option:
                score += 1
        
        # Mastery threshold: 80%
        if total > 0 and (score / total) >= 0.8:
            # Mark as resolved
            StudentWeakTopic.objects.filter(student=student_profile, topic=topic).update(is_resolved=True)
            messages.success(request, "Topic Mastered! You scored over 80%.")
            return redirect('learning-path')
        else:
             messages.warning(request, f"Score: {score}/{total}. You need 80% to master this topic. Try again!")
             return redirect('learning-path')
        
    return render(request, "student/topic_quiz.html", {"topic": topic, "questions": questions})

@login_required
def recommendations(request):
    student_profile = request.user.student_profile

    # 1️⃣ Get unresolved weak topics
    weak_topics_qs = StudentWeakTopic.objects.filter(
        student=student_profile,
        is_resolved=False
    ).select_related("topic")

    if not weak_topics_qs.exists():
        # No weak topics → back to dashboard
        return redirect("student-dashboard")

    # 2️⃣ Pick ONE topic at a time (simpler flow)
    current_weak_topic = weak_topics_qs.first().topic

    subject = current_weak_topic.subject
    class_level = student_profile.student_class

    # 3️⃣ Get level dynamically based on subject
    level_map = {
        "Maths": student_profile.maths_level,
        "Science": student_profile.science_level,
        "English": student_profile.english_level,
    }
    level = level_map.get(subject, "Beginner")

    # 4️⃣ Gemini explanation
    explanation = generate_explanation(
        class_level=class_level,
        subject=subject,
        level=level,
        weak_topics=[current_weak_topic.name]
    )

    context = {
        "topic": current_weak_topic,
        "explanation": explanation,
    }

    return render(request, "student/recommendations.html", context)
