
import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PadhaiMate.settings')
django.setup()

from student.models import Topic

def check_system():
    print("--- TOPIC DATA ---")
    for t in Topic.objects.all():
        print(f"Topic: '{t.name}' | Subject: '{t.subject}'")

    print("\n--- GEMINI CONFIG ---")
    key = getattr(settings, 'GEMINI_API_KEY', None)
    if key:
        print(f"API Key present: {key[:5]}... (Length: {len(key)})")
    else:
        print("❌ API Key MISSING in settings.")

if __name__ == "__main__":
    check_system()
