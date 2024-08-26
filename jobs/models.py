from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=255, default="none")
    company = models.CharField(max_length=255, default="none")  # Name of the company offering the job
    location = models.CharField(max_length=255, default="none")
    description = models.TextField()
    responsibilities = models.TextField(help_text="List of job responsibilities", default="none")  # New field for responsibilities
    requirements = models.TextField(help_text="List of job requirements", default="none")  # New field for requirements
    salary = models.CharField(max_length=100, blank=True, null=True, help_text="Salary range or amount")  # Optional salary field
    posted_date = models.DateField(auto_now_add=True, blank=True, null=True)
    application_deadline = models.DateField(null=True, blank=True, help_text="Deadline to apply for the job")  # New field for application deadline

    def __str__(self):
        return f"{self.title} at {self.company}"

    class Meta:
        ordering = ['-posted_date']  # Orders job listings by the most recent first
