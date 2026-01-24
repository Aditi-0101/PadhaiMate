import os
import sys
import django
from django.test import RequestFactory, Client
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware

# Add project root to path
sys.path.append(os.getcwd())

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PadhaiMate.settings")
try:
    django.setup()
except Exception:
    pass

from student.models import Topic, Question, StudentProfile, StudentWeakTopic, LearningContent
from student.views import quiz

def verify():
    print("VERIFICATION_START")
    # 1. Setup Data
    print("Setting up test data...")
    user, created = User.objects.get_or_create(username="test_student", first_name="Test", last_name="Student")
    if created:
        user.set_password("password")
        user.save()
        StudentProfile.objects.create(
            user=user, 
            student_class=6,
            maths_level="Beginner",
            science_level="Beginner",
            english_level="Beginner"
        )
    
    student_profile = user.student_profile
    
    # Ensure topics exist (from populate script)
    try:
        topic = Topic.objects.get(name="Probability")
        print(f"Target Topic: {topic}")
    except Topic.DoesNotExist:
        print("Error: Topics not populated. Run populate_topics.py first.")
        return

    # Find questions for this topic
    questions = Question.objects.filter(topic=topic)
    if not questions.exists():
        print("Error: No questions found for Probability.")
        return
    
    q1 = questions.first()
    wrong_answer = "Z" # Assuming Z is always wrong since choices are A,B,C,D
    
    print(f"Testing with Question: {q1.question_text} (Correct: {q1.correct_option})")

    # 2. Simulate Quiz Submission via Client
    client = Client()
    client.force_login(user)
    
    # Pre-set session for quiz
    session = client.session
    session['answers'] = {str(q1.id): wrong_answer} # Wrong answer
    session.save()
    
    print("Submitting quiz with wrong answer...")
    # Simulate the "finish" action
    response = client.post('/student/quiz', {
        'action': 'finish',
        'question_id': q1.id,
        'answer': wrong_answer,
        'current_index': 1
    }, follow=True)
    
    if response.status_code == 200:
        print("Quiz submitted successfully.")
    else:
        print(f"Quiz submission failed: {response.status_code}")

    # 3. Verify Weak Topic Created
    weak_topic_exists = StudentWeakTopic.objects.filter(
        student=student_profile,
        topic=topic,
        is_resolved=False
    ).exists()
    
    if weak_topic_exists:
        print("SUCCESS: StudentWeakTopic created for 'Probability'.")
    else:
        print("FAILURE: StudentWeakTopic NOT created.")
        
    # 4. Verify Content Availability
    contents = LearningContent.objects.filter(topic=topic)
    print(f"Found {contents.count()} learning content items for this topic.")
    
    print("\nVerification Complete.")

if __name__ == "__main__":
    verify()
