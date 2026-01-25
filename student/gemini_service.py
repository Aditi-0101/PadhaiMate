import google.generativeai as genai
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class AIService:
    @staticmethod
    def configure():
        """Configures the Gemini API with the settings key."""
        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            return True
        except Exception as e:
            logger.error(f"Failed to configure Gemini API: {e}")
            return False

    @staticmethod
    def generate_study_plan(student_profile, weak_topics):
        """
        Generates a personalized study plan using Gemini.
        Returns:
            dict: JSON object with 'day_1', 'day_2', 'day_3' keys.
        """
        if not AIService.configure():
            return None

        # Focus on the FIRST weak topic to ensure quality (as per requirement)
        target_topic = weak_topics[0]
        concepts = target_topic.weak_concepts if target_topic.weak_concepts else "General understanding"

        prompt = f"""
        You are PadhaiMate AI.
        Student: Class {student_profile.student_class}
        Subject: {target_topic.topic.subject}
        Weak Topic: {target_topic.topic.name}
        Weak Concepts: {concepts}
        
        TASK:
        Create a STRICT 3-Day Mastery Plan for this topic.
        Return ONLY valid JSON. No Markdown. No extra text.
        
        JSON Structure:
        {{
            "why_tricky": "1 sentence explanation",
            "day_1": {{
                "title": "Unpack & Understand",
                "explanation": "Clear concept explanation",
                "example": "1 simple example",
                "practice": "1 specific practice task"
            }},
            "day_2": {{
                "title": "Connect & Visualize",
                "revision": "1 sentence revision",
                "examples": "2 distinct examples",
                "visual_idea": "Describe a visual helper/diagram"
            }},
            "day_3": {{
                "title": "Master & Apply",
                "recap": "Quick recap",
                "quiz_prep": "Mini quiz question idea",
                "confidence_note": "Encouraging closing note"
            }},
            "real_life_application": "1 cool real-world usage"
        }}
        """

        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            # Strip markdown code blocks if present
            text = response.text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                 text = text.split("```")[1].split("```")[0]
            
            return text.strip()
        except Exception as e:
            logger.error(f"Gemini generation failed: {e}")
            return None
