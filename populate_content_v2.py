import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PadhaiMate.settings")
django.setup()

from student.models import Topic, LearningContent

def populate():
    print("Starting Content Population V2...")
    
    # Clear existing content to avoid duplicates and ensure clean tagging
    LearningContent.objects.all().delete()
    
    # helper for upsert
    def add_content(topic_name, subject, title, content_type, text_content, image_url=None, video_url=None, concept_tag=""):
        try:
            topic_obj = Topic.objects.get(name=topic_name, subject=subject)
            LearningContent.objects.create(
                topic=topic_obj,
                title=title,
                content_type=content_type,
                text_content=text_content,
                image_url=image_url,
                video_url=video_url,
                concept_tag=concept_tag
            )
            print(f"[Created] {title} - {concept_tag}")
        except Topic.DoesNotExist:
            print(f"[Error] Topic {topic_name} not found.")

    # --- MATHS ---
    
    # Probability (Enhanced)
    add_content("Probability", "Maths", "Ludo Dice", "real_life", 
        "Think about playing Ludo. When you roll a dice, getting a 6 is just luck! You have 1 chance out of 6 numbers.", 
        "/static/images/ludo_dice.png", concept_tag="probability_basics")

    # Geometry
    add_content("Geometry", "Maths", "Perimeter vs Area", "concept", 
        "Perimeter is the distance AROUND a shape (like a fence). Area is the space INSIDE a shape (like a carpet).", concept_tag="area_perimeter")
    
    add_content("Geometry", "Maths", "Real Life Geometry", "real_life", 
        "Your classroom blackboard is a Rectangle. The clock on the wall is a Circle. Geometry is everywhere!",
        "https://www.mathsisfun.com/images/quadrilaterals.svg", concept_tag="shapes")

    # --- SCIENCE ---

    # Force and Motion
    add_content("Force and Motion", "Science", "What is Force?", "concept",
        "A Force is simply a PUSH or a PULL. It can make things move, stop, or change shape.",
        "/static/images/hand_push_box.png", concept_tag="force_definition")
    
    add_content("Force and Motion", "Science", "Push and Pull", "visual",
        "Pushing a swing makes it go forward. Pulling a door opens it.",
        "/static/images/swing_push.png", concept_tag="push_pull")
    
    add_content("Force and Motion", "Science", "Friction", "real_life",
        "Why does a rolling ball stop? Because of Friction! It is a force that slows things down, like your shoes grieving the floor.",
        "/static/images/friction_shoe.png", concept_tag="friction")

    # Light
    add_content("Light", "Science", "Light Travels Straight", "concept",
        "Light always travels in a straight line. It cannot bend around corners unless it hits a mirror.", concept_tag="light_properties")
    
    add_content("Light", "Science", "Shadows", "visual",
        "A shadow is formed when an object blocks light. If you stand in the sun, your body blocks the light and makes a dark shadow on the ground.",
        "/static/images/shadow_tree.png", concept_tag="shadows")

    # --- ENGLISH ---

    # Grammar
    add_content("Grammar", "English", "Subject and Verb", "concept", 
        "Every sentence has a 'Doer' (Subject) and an 'Action' (Verb). Example: 'Ram (Subject) eats (Verb) an apple.'", concept_tag="grammar_basics")
    
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
    populate()
