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

from student.models import Topic, LearningContent

def verify_content():
    print("VERIFICATION_V2_START")
    
    # Check specifically for "Force and Motion" as requested
    try:
        topic = Topic.objects.get(name="Force and Motion")
        print(f"Topic Found: {topic}")
        
        contents = LearningContent.objects.filter(topic=topic)
        print(f"Content Items: {contents.count()}")
        
        for c in contents:
            print(f" - [{c.content_type}] {c.title}: {c.text_content[:50]}...")
            
        if contents.count() >= 3:
            print("SUCCESS: Rich content available for Force and Motion.")
        else:
            print("WARNING: Content count low.")
            
    except Topic.DoesNotExist:
        print("FAILURE: Topic 'Force and Motion' not found.")
        
    print("VERIFICATION_V2_END")

if __name__ == "__main__":
    verify_content()
