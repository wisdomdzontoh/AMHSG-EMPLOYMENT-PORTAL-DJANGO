from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    posted_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title

