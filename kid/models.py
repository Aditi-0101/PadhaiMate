from django.db import models
from django.contrib.auth.models import User

class Kid(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    kid_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    class_level = models.CharField(max_length=20)

    def __str__(self):
        return self.kid_id
