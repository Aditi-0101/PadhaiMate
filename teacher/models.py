from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class TeacherProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="teacher_profile"
    )
    subject = models.CharField(max_length=50)
    classes = models.CharField(
        max_length=20,
        help_text="Comma separated classes e.g. 6,7,8"
    )

    def __str__(self):
        return f"{self.user.username} - {self.subject}"