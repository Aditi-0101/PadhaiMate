import os
import django
import sys
from django.contrib.messages import get_messages

# Add project root to path
sys.path.append(os.getcwd())

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PadhaiMate.settings")
try:
    django.setup()
except Exception:
    pass

from student.models import Topic, Question, StudentProfile, StudentWeakTopic
from student.views import submit_topic_practice
from django.test import RequestFactory
from django.contrib.auth.models import User
from django.contrib.sessions.middleware import SessionMiddleware

def verify_inline_quiz():
    print("VERIFICATION_INLINE_QUIZ_START")
    
    # 1. Setup
    user, _ = User.objects.get_or_create(username="test_student", first_name="Test")
    student_profile = user.student_profile
    topic = Topic.objects.get(name="Force and Motion")
    
    # Ensure weak topic exists
    wt, created = StudentWeakTopic.objects.get_or_create(student=student_profile, topic=topic)
    wt.is_resolved = False
    wt.save()
    print(f"Testing with Topic: {topic.name}, Resolved: {wt.is_resolved}")

    # Get Questions
    questions = Question.objects.filter(topic=topic)[:5]
    if len(questions) < 3:
        print("Not enough questions to test mastery.")
        return

    # 2. Simulate POST Request (Correct Answers)
    factory = RequestFactory()
    data = {'topic_id': topic.id}
    for q in questions:
        data[f'q_{q.id}'] = q.correct_option # Mark all correct
        
    request = factory.post('/student/submit-topic-practice/', data)
    request.user = user
    
    # Add session and messages support
    middleware = SessionMiddleware(lambda x: None)
    middleware.process_request(request)
    request.session.save()
    
    # Mock messages
    class MockMessage:
        def add(self, level, message, extra_tags):
            print(f"Message ({level}): {message}") 

    request._messages = MockMessage()

    # 3. Call View
    print("Submitting perfect score...")
    submit_topic_practice(request)

    # 4. Verify Resolution
    wt.refresh_from_db()
    if wt.is_resolved:
        print("SUCCESS: Topic marked as resolved after passing quiz.")
    else:
        print("FAILURE: Topic NOT resolved.")

    print("VERIFICATION_INLINE_QUIZ_END")

if __name__ == "__main__":
    verify_inline_quiz()
