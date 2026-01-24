import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PadhaiMate.settings")
django.setup()

from student.models import Topic, LearningContent

def populate_rich_content():
    print("Starting Content Population V2...")
    
    # helper for upsert
    def add_content(topic_name, subject, title, c_type, text, img=None):
        try:
            topic = Topic.objects.get(name=topic_name, subject=subject)
            obj, created = LearningContent.objects.update_or_create(
                topic=topic,
                title=title,
                content_type=c_type,
                defaults={
                    "text_content": text,
                    "image_url": img
                }
            )
            print(f"[{'Created' if created else 'Updated'}] {topic.name} -> {title}")
        except Topic.DoesNotExist:
            print(f"[Skipped] Topic not found: {topic_name} ({subject})")

    # --- MATHS ---
    
    # Probability (Enhanced)
    add_content("Probability", "Maths", "Ludo Dice", "real_life", 
        "Think about playing Ludo. When you roll a dice, getting a 6 is just luck! You have 1 chance out of 6 numbers.", 
        "/static/images/ludo_dice.png")

    # Geometry
    add_content("Geometry", "Maths", "Perimeter vs Area", "concept", 
        "Perimeter is the distance AROUND a shape (like a fence). Area is the space INSIDE a shape (like a carpet).")
    
    add_content("Geometry", "Maths", "Real Life Geometry", "real_life", 
        "Your classroom blackboard is a Rectangle. The clock on the wall is a Circle. Geometry is everywhere!",
        "https://www.mathsisfun.com/images/quadrilaterals.svg")

    # --- SCIENCE ---

    # Force and Motion
    add_content("Force and Motion", "Science", "What is Force?", "concept",
        "A Force is simply a PUSH or a PULL. It can make things move, stop, or change shape.",
        "/static/images/hand_push_box.png")
    
    add_content("Force and Motion", "Science", "Push and Pull", "visual",
        "Pushing a swing makes it go forward. Pulling a door opens it.",
        "/static/images/swing_push.png")
    
    add_content("Force and Motion", "Science", "Friction", "real_life",
        "Why does a rolling ball stop? Because of Friction! It is a force that slows things down, like your shoes grieving the floor.",
        "/static/images/friction_shoe.png")

    # Light
    add_content("Light", "Science", "Light Travels Straight", "concept",
        "Light always travels in a straight line. It cannot bend around corners unless it hits a mirror.")
    
    add_content("Light", "Science", "Shadows", "visual",
        "A shadow is formed when an object blocks light. If you stand in the sun, your body blocks the light and makes a dark shadow on the ground.",
        "/static/images/shadow_tree.png")

    # --- ENGLISH ---

    # Grammar
    add_content("Grammar", "English", "Subject and Verb", "concept", 
        "Every sentence has a 'Doer' (Subject) and an 'Action' (Verb). Example: 'Ram (Subject) eats (Verb) an apple.'")
    
    add_content("Grammar", "English", "Tenses made easy", "visual",
        "Past: Yesterday I played. Present: Today I play. Future: Tomorrow I will play.")

    # Vocabulary
    add_content("Vocabulary", "English", "Synonyms (Same meaning)", "concept",
        "Synonyms are words with the same meaning. \nHappy = Joyful \nBig = Huge \nSmall = Tiny")
    
    add_content("Vocabulary", "English", "Antonyms (Opposites)", "visual",
        "Hot x Cold \nDay x Night \nUp x Down",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Thermometer_hot_and_cold.svg/320px-Thermometer_hot_and_cold.svg.png")

    print("Content Population V2 Complete.")

if __name__ == "__main__":
    populate_rich_content()
