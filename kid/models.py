# kids/models.py
from django.db import models

class Kid(models.Model):
    kid_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    class_level = models.IntegerField()

    def __str__(self):
        return f"{self.kid_id} - {self.name}"
