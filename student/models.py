from django.db import models
from django.contrib.auth.models import User

# Create your models here.

CLASS_CHOICES = [
    (6, "Class 6"),
    (7, "Class 7"),
    (8, "Class 8"),
]

OPTION_CHOICES = [
    ("A", "A"),
    ("B", "B"),
    ("C", "C"),
    ("D", "D"),
]

DIFFICULTY_CHOICES = [
    ("easy", "Easy"),
    ("medium", "Medium"),
    ("hard", "Hard"),
]

class StudentProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student_profile"
    )
    student_class = models.IntegerField(choices=CLASS_CHOICES)
    maths_level = models.CharField(
        max_length=20,
        choices=[
            ("Beginner", "Beginner"),
            ("Intermediate", "Intermediate"),
            ("Advanced", "Advanced"),
        ],
        default="Beginner"
    )

    science_level = models.CharField(
        max_length=20,
        choices=[
            ("Beginner", "Beginner"),
            ("Intermediate", "Intermediate"),
            ("Advanced", "Advanced"),
        ],
        default="Beginner"
    )

    english_level = models.CharField(
        max_length=20,
        choices=[
            ("Beginner", "Beginner"),
            ("Intermediate", "Intermediate"),
            ("Advanced", "Advanced"),
        ],
        default="Beginner"
    )

    def __str__(self):
        return f"{self.user.username} - Class {self.student_class}"

class Topic(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=50)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.subject})"

class LearningContent(models.Model):
    CONTENT_TYPES = [
        ('concept', 'Concept Explanation'),
        ('visual', 'Visual Aid'),
        ('real_life', 'Real-life Example'),
    ]
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='contents')
    title = models.CharField(max_length=200)
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPES)
    text_content = models.TextField()
    image_url = models.URLField(blank=True, null=True, help_text="URL for image/diagram")
    video_url = models.URLField(blank=True, null=True, help_text="YouTube URL or similar")
    concept_tag = models.CharField(max_length=50, blank=True, help_text="Tag for specific concept matching (e.g. 'friction')")

    def __str__(self):
        return f"{self.title} ({self.topic.name})"

class StudentWeakTopic(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    is_resolved = models.BooleanField(default=False)
    weak_concepts = models.TextField(blank=True, help_text="Comma-separated list of weak concept tags")
    study_plan = models.JSONField(blank=True, null=True, help_text="AI-generated 3-day study plan")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.user.username} - {self.topic.name}"

class Question(models.Model):
    class_level = models.IntegerField(choices=CLASS_CHOICES)
    subject_name = models.CharField(max_length=50)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True)
    concept_tag = models.CharField(max_length=50, blank=True, help_text="Tag for specific concept (e.g. 'friction')")

    question_text = models.TextField()

    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)

    correct_option = models.CharField(
    max_length=1,
    choices=OPTION_CHOICES
    )

    def __str__(self):
        return f"Class {self.class_level} - {self.subject_name} ({self.difficulty})"

class AssessmentResult(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    subject_name = models.CharField(max_length=50)

    easy_correct = models.IntegerField(default=0)
    medium_correct = models.IntegerField(default=0)
    hard_correct = models.IntegerField(default=0)

    total_questions = models.IntegerField(null=True, blank=True)
    time_taken = models.IntegerField(help_text="seconds")

    created_at = models.DateTimeField(auto_now_add=True)

