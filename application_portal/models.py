from django.db import models
from django.contrib.auth.models import User
from jobs.models import Job

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #payment_status = models.BooleanField(default=False)
    job_title = models.ForeignKey(Job, on_delete=models.CASCADE, blank=True)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    date_of_birth = models.DateField()
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField()
    # Add more fields as per your form's structure
    
    
    
    date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.full_name - self.job_title
    

