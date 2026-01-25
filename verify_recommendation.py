import os
import django
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PadhaiMate.settings')
django.setup()

# Ensure testserver is allowed
if 'testserver' not in settings.ALLOWED_HOSTS:
    settings.ALLOWED_HOSTS = list(settings.ALLOWED_HOSTS) + ['testserver']

from django.test import RequestFactory, Client
from django.contrib.auth.models import User
from student.models import StudentProfile, Topic, Question, StudentWeakTopic, LearningContent
from student.services import RecommendationService
from student.views import recommendation

def verify_recommendation_flow():
    print("--- Verifying Recommendation Architecture ---")

    # 1. Setup Data
    print("1. Setting up test data...")
    user, created = User.objects.get_or_create(username="test_rec_user")
    if created:
        user.set_password("testpass")
        user.save()
    
    profile, _ = StudentProfile.objects.get_or_create(
        user=user,
        defaults={
            'student_class': 8,
            'maths_level': 'Beginner',
            'science_level': 'Intermediate',
            'english_level': 'Advanced'
        }
    )

    # Clean previous weak topics
    StudentWeakTopic.objects.filter(student=profile).delete()

    topic, _ = Topic.objects.get_or_create(name="Test Topic Rec", subject="Maths")
    
    q1 = Question.objects.create(
        question_text="Q1", option_a="A", option_b="B", option_c="C", option_d="D",
        correct_option="A", topic=topic, concept_tag="concept_x",
        class_level=8, subject_name="Maths", difficulty="easy"
    )
    q2 = Question.objects.create(
        question_text="Q2", option_a="A", option_b="B", option_c="C", option_d="D",
        correct_option="B", topic=topic, concept_tag="concept_y",
        class_level=8, subject_name="Maths", difficulty="medium"
    )

    # 2. Verify Service Logic (Calculation)
    print("2. Verifying RecommendationService.calculate_weak_areas...")
    all_questions = [q1, q2]
    # Answers: Q1 Correct (A), Q2 Incorrect (C instead of B)
    answers = {
        str(q1.id): "A",
        str(q2.id): "C" 
    }
    
    weak_areas = RecommendationService.calculate_weak_areas(all_questions, answers)
    
    assert topic in weak_areas, "Topic not identified as weak"
    assert "concept_y" in weak_areas[topic], "Incorrect concept not identified"
    assert "concept_x" not in weak_areas[topic], "Correct concept incorrectly marked weak"
    print("   [Pass] Service Calculation Logic")

    # 3. Verify Service Logic (Storage)
    print("3. Verifying RecommendationService.store_weak_areas...")
    RecommendationService.store_weak_areas(profile, weak_areas)
    
    wt = StudentWeakTopic.objects.get(student=profile, topic=topic)
    assert "concept_y" in wt.weak_concepts, "Weak concept not stored in DB"
    print("   [Pass] Service Storage Logic")

    # 4. Verify View (GET /student/recommendation/)
    print("4. Verifying Recommendation View...")
    client = Client()
    client.force_login(user)
    response = client.get('/student/recommendation/')
    
    print(f"Status Code: {response.status_code}")
    print(f"Status Code: {response.status_code}")
    if response.status_code != 200:
        with open("error_response.html", "wb") as f:
            f.write(response.content)
        print("Error response saved to error_response.html")
    
    assert response.status_code == 200, f"View returned {response.status_code}"
    # Check context
    content = response.content.decode('utf-8')
    assert "Test Topic Rec" in content, "Weak topic name not found in rendered page"
    assert "concept_y" in content, "Weak concept tag not found in rendered page"
    assert "Intermediate" in content, "Science level (Intermediate) not found in page"
    
    print("   [Pass] Recommendation View loads correctly")

    print("\n[SUCCESS] Verification Successful!")

if __name__ == "__main__":
    try:
        verify_recommendation_flow()
    except AssertionError as e:
        print(f"[FAIL] Verification Failed: {e}")
    except Exception as e:
        print(f"[ERROR]: {e}")
