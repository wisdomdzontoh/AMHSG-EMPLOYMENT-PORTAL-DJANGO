from django.db import models
from django.contrib.auth.models import User
from jobs.models import Job

class Application(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #payment_status = models.BooleanField(default=False)
    job_title = models.ForeignKey(Job, on_delete=models.CASCADE, blank=True)
    full_name = models.CharField(max_length=255, default="none")
    email = models.EmailField(default="none")
    phone_number = models.CharField(max_length=15, default="0245325587")
    address = models.TextField(default="none")
    #date_of_birth = models.DateField(auto_now_add=True)
    #resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(default="none")
    # Add more fields as per your form's structure
    
    
    
    date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.full_name - self.job_title
    

