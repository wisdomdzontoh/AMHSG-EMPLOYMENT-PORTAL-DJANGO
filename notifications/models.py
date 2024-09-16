from django.db import models
from django.contrib.auth.models import User

class Notification(models.Model):
    message = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

