
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PadhaiMate.settings')
django.setup()

from student.models import Topic, Question

def verify_data():
    print("Verifying Topic Subjects...")
    topics = Topic.objects.all()
    for t in topics:
        print(f"Topic: {t.name}, Subject: {t.subject}")

    print("\nVerifying Question Mappings...")
    questions = Question.objects.exclude(topic=None)
    mismatches = 0
    for q in questions:
        if q.subject_name != q.topic.subject:
            print(f"MISMATCH: Question {q.id} ({q.subject_name}) -> Topic {q.topic.name} ({q.topic.subject})")
            mismatches += 1
            # OPTIONAL: Auto-fix? 
            # q.topic.subject = q.subject_name
            # q.topic.save() 
            # Be careful with auto-fixing topics as they might belong to multiple? 
            # In this app, topics seem subject-specific.

    if mismatches == 0:
        print("✅ No mismatches found.")
    else:
        print(f"❌ Found {mismatches} mismatches.")

if __name__ == "__main__":
    verify_data()
