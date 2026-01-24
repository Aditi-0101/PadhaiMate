import os
import django
import random

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PadhaiMate.settings")
django.setup()

from student.models import Topic, Question, LearningContent

def populate_data():
    # 1. Create Topics
    topics_data = [
        {"name": "Probability", "subject": "Maths", "description": "Understanding chance and uncertainty."},
        {"name": "Geometry", "subject": "Maths", "description": "Shapes, sizes, relative position of figures, and properties of space."},
        {"name": "Force and Motion", "subject": "Science", "description": "How things move and what makes them move."},
        {"name": "Light", "subject": "Science", "description": "Understanding reflection, shadows, and visibility."},
        {"name": "Grammar", "subject": "English", "description": "Rules of language structure."},
        {"name": "Vocabulary", "subject": "English", "description": "Understanding words and meanings."},
    ]

    topics = {}
    for t_data in topics_data:
        topic, created = Topic.objects.get_or_create(
            name=t_data["name"],
            subject=t_data["subject"],
            defaults={"description": t_data["description"]}
        )
        topics[(t_data["subject"], t_data["name"])] = topic
        print(f"Topic {'Created' if created else 'Exists'}: {topic}")

    # 2. Assign Topics to Questions (Simple Keyword matching)
    questions = Question.objects.all()
    count = 0
    for q in questions:
        subject = q.subject_name
        assigned_topic = None
        
        # Simple heuristic mapping
        q_text = q.question_text.lower()
        if subject == "Maths":
            if "angle" in q_text or "triangle" in q_text or "circle" in q_text or "shape" in q_text:
                 assigned_topic = topics.get(("Maths", "Geometry"))
            else:
                 # Default logic or random for demo if no keyword matches to ensure flow coverage
                 assigned_topic = topics.get(("Maths", "Probability"))
        elif subject == "Science":
            if "light" in q_text or "shadow" in q_text or "mirror" in q_text:
                assigned_topic = topics.get(("Science", "Light"))
            else:
                assigned_topic = topics.get(("Science", "Force and Motion"))
        elif subject == "English":
            if "noun" in q_text or "verb" in q_text or "article" in q_text or "tense" in q_text:
                assigned_topic = topics.get(("English", "Grammar"))
            else:
                assigned_topic = topics.get(("English", "Vocabulary"))
        
        if assigned_topic:
            q.topic = assigned_topic
            q.save()
            count += 1
            
    print(f"Assigned topics to {count} questions.")

    # 3. Add Learning Content
    # Probability
    prob_topic = topics.get(("Maths", "Probability"))
    if prob_topic:
        LearningContent.objects.get_or_create(
            topic=prob_topic,
            title="What is Probability?",
            content_type="concept",
            defaults={
                "text_content": "Probability is simply how likely something is to happen. When you toss a coin, there are two chances: Heads or Tails. So, the chance of getting Heads is 1 out of 2.",
                "image_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Coin_tossing.jpg/320px-Coin_tossing.jpg"
            }
        )
        LearningContent.objects.get_or_create(
            topic=prob_topic,
            title="Coin Toss Experiment",
            content_type="visual",
            defaults={
                "text_content": "Imagine flipping a coin. It can land on only one side. This is called an outcome.",
                "image_url": "https://www.mathsisfun.com/data/images/probability-line.gif"
            }
        )
        LearningContent.objects.get_or_create(
            topic=prob_topic,
            title="Weather Forecast",
            content_type="real_life",
            defaults={
                "text_content": "When the weather app says '50% chance of rain', it is using probability! It means it might rain or it might not, equally likely.",
            }
        )

    # Geometry
    geo_topic = topics.get(("Maths", "Geometry"))
    if geo_topic:
        LearningContent.objects.get_or_create(
            topic=geo_topic,
            title="Polygons",
            content_type="visual",
            defaults={
               "text_content": "A polygon is a closed shape with straight sides. Triangles, squares, and rectangles are all polygons.",
               "image_url": "https://www.mathsisfun.com/images/polygons-simple.svg"
            }
        )
    
    # Grammar
    grammar_topic = topics.get(("English", "Grammar"))
    if grammar_topic:
        LearningContent.objects.get_or_create(
            topic=grammar_topic,
            title="Nouns",
            content_type="concept",
            defaults={
                "text_content": "A Noun is a naming word. It can be a name of a person (Ram), place (Delhi), animal (Tiger), or thing (Table).",
            }
        )

    print("Learning Content populated.")

if __name__ == "__main__":
    populate_data()
