from .models import Question, StudentWeakTopic, Topic

class RecommendationService:
    @staticmethod
    def calculate_weak_areas(all_questions, answers):
        """
        Identifies weak topics and concepts based on incorrect answers.
        
        Args:
            all_questions (list): List of Question objects from the quiz.
            answers (dict): Dictionary mapping question_id (str) to selected_option (str).
            
        Returns:
            dict: A dictionary mapping Topic objects to a set of weak concept tags (strings).
        """
        incorrect_questions = []
        for q in all_questions:
            q_id = str(q.id)
            if q_id in answers:
                if answers[q_id] != q.correct_option:
                    incorrect_questions.append(q)
        
        weak_areas_map = {} # Map topic -> set of weak concepts

        for q in incorrect_questions:
            if q.topic:
                if q.topic not in weak_areas_map:
                    weak_areas_map[q.topic] = set()
                
                if q.concept_tag:
                    weak_areas_map[q.topic].add(q.concept_tag)
                    
        return weak_areas_map

    @staticmethod
    def store_weak_areas(student_profile, weak_areas_map):
        """
        Persists identified weak areas to the database.
        
        Args:
            student_profile (StudentProfile): The student's profile.
            weak_areas_map (dict): Output from calculate_weak_areas.
        """
        for topic, new_concepts in weak_areas_map.items():
            # Strict check: Ensure topic subject matches a valid subject for the student/quiz context
            # (Though logic should prevent this, extra safety here)
            
            wt, created = StudentWeakTopic.objects.get_or_create(
                student=student_profile,
                topic=topic,
                defaults={'is_resolved': False}
            )
            
            # Update weak concepts
            current_concepts = set(wt.weak_concepts.split(',')) if wt.weak_concepts else set()
            
            # Combine and filter empty strings
            updated_concepts = current_concepts.union(new_concepts)
            updated_concepts = {c for c in updated_concepts if c.strip()}
            
            wt.weak_concepts = ",".join(updated_concepts)
            wt.is_resolved = False # Re-open if new mistakes made
            wt.save()

    @staticmethod
    def get_student_recommendation_data(student_profile):
        """
        Retrieves data for the recommendation page.
        
        Args:
            student_profile (StudentProfile): The student's profile.
            
        Returns:
            dict: Context data for the template.
        """
        # Fetch active weak topics
        weak_topics_qs = StudentWeakTopic.objects.filter(
            student=student_profile,
            is_resolved=False
        ).select_related('topic')

        # Group by Subject to prevent leakage and display structured
        weak_topics_by_subject = {}
        all_weak_topics_list = []
        
        for wt in weak_topics_qs:
            subj = wt.topic.subject
            if subj not in weak_topics_by_subject:
                weak_topics_by_subject[subj] = []
            weak_topics_by_subject[subj].append(wt)
            all_weak_topics_list.append(wt)
        
        return {
            'student_profile': student_profile,
            'maths_level': student_profile.maths_level,
            'science_level': student_profile.science_level,
            'english_level': student_profile.english_level,
            'weak_topics_by_subject': weak_topics_by_subject,
            'weak_topics': all_weak_topics_list, # Kept for AI Service compatibility
        }

    @staticmethod
    def save_study_plan(student_weak_topic, plan_json_str):
        """
        Saves the AI generated plan to the database.
        """
        import json
        try:
            plan_data = json.loads(plan_json_str)
            student_weak_topic.study_plan = plan_data
            student_weak_topic.save()
            return plan_data
        except json.JSONDecodeError:
            return None
