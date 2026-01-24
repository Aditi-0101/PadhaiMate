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

class Question(models.Model):
    class_level = models.IntegerField(choices=CLASS_CHOICES)
    subject_name = models.CharField(max_length=50)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    topic_name = models.CharField(max_length=100, null=True, blank=True)

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

