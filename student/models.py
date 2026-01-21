from django.db import models
from django.contrib.auth.models import User

# Create your models here.

CLASS_CHOICES = [
    (6, "Class 6"),
    (7, "Class 7"),
    (8, "Class 8"),
]


class StudentProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student_profile"
    )
    student_class = models.IntegerField(choices=CLASS_CHOICES)

    def __str__(self):
        return f"{self.user.username} - Class {self.student_class}"