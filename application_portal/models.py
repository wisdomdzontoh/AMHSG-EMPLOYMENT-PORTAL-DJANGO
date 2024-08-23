from django.db import models
from django.contrib.auth.models import User
from jobs.models import Job

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_status = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    job_title = models.ForeignKey(Job, on_delete=models.CASCADE, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name