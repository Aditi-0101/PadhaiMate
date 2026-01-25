import os
import django
import sys

# Add project root to path
sys.path.append(os.getcwd())

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PadhaiMate.settings")
try:
    django.setup()
except Exception:
    pass

from student.models import Question

def tag_questions():
    print("Tagging Questions...")
    
    # 1. Force and Motion (ID 4 is usually Friction)
    try:
        q_friction = Question.objects.get(id=4)
        q_friction.concept_tag = "friction"
        q_friction.question_text = "Why does a rolling ball stop on its own?" # Ensure text matches intent
        q_friction.save()
        print(f"Tagged Question {q_friction.id}: friction")
    except Question.DoesNotExist:
        print("Question 4 not found")

    # 2. Force (ID 1 is usually Push/Pull)
    try:
        q_force = Question.objects.get(id=1)
        q_force.concept_tag = "push_pull"
        q_force.save()
        print(f"Tagged Question {q_force.id}: push_pull")
    except Question.DoesNotExist:
        print("Question 1 not found")

    # 3. Light (ID 3 is usually Shadow)
    try:
        q_shadow = Question.objects.get(id=3)
        q_shadow.concept_tag = "shadows"
        q_shadow.save()
        print(f"Tagged Question {q_shadow.id}: shadows")
    except Question.DoesNotExist:
        print("Question 3 not found")

    print("Tagging Complete.")

if __name__ == "__main__":
    tag_questions()
