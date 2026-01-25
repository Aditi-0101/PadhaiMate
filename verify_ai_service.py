# Helper script to quickly verify AI connectivity without running the full server flow
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PadhaiMate.settings')
django.setup()

from student.ai_service import AIService
from student.models import StudentProfile, Topic, StudentWeakTopic
from django.contrib.auth.models import User

def test_ai_connection():
    print("--- Testing Gemini AI Service ---")
    
    # 1. Create Dummy Data
    user, _ = User.objects.get_or_create(username="ai_tester")
    profile, _ = StudentProfile.objects.get_or_create(
        user=user, 
        defaults={
            'student_class': 8, 
            'maths_level': 'Intermediate',
            'science_level': 'Beginner', 
            'english_level': 'Advanced'
        }
    )
    
    topic, _ = Topic.objects.get_or_create(name="Friction", subject="Science")
    wt = StudentWeakTopic(student=profile, topic=topic, weak_concepts="static friction, kinetic friction")
    
    # 2. Call Service
    print("Sending prompt to Gemini...")
    try:
        response = AIService.generate_study_plan(profile, [wt])
        
        if response:
            print("\n✅ AI Response Received:")
            print("-" * 40)
            print(response[:500] + "...") # Print start of response
            print("-" * 40)
            if "<div" in response:
                 print("   [Pass] Output format contains HTML tags")
            else:
                 print("   [Warn] Output format might not be HTML")
        else:
            print("❌ AI returned None (Check configuration or quota)")
            
    except Exception as e:
        print(f"❌ Exception during AI call: {e}")

if __name__ == "__main__":
    test_ai_connection()
