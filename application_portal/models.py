from django.db import models
from django.contrib.auth.models import User
from jobs.models import Job
from django.utils import timezone

class PersonalInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_title = models.ForeignKey(Job, on_delete=models.CASCADE, blank=True, null=True)  # Add null=True if job_title can be empty
    title = models.CharField(max_length=10, choices=[('mr', 'Mr'), ('mrs', 'Mrs'), ('ms', 'Ms')])
    email = models.EmailField()
    first_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    other_names = models.CharField(max_length=100, blank=True, null=True)
    dob = models.DateField()
    telephone = models.CharField(max_length=15)
    birthplace = models.CharField(max_length=100)
    marital_status = models.CharField(max_length=20, choices=[('single', 'Single'), ('married', 'Married'), ('divorced', 'Divorced/Separated'), ('widow', 'Widow')])
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')])
    fathers_name = models.CharField(max_length=100)
    fathers_occupation = models.CharField(max_length=100)
    mothers_name = models.CharField(max_length=100)
    mothers_occupation = models.CharField(max_length=100)
    next_of_kin = models.CharField(max_length=100)
    next_of_kin_occupation = models.CharField(max_length=100)
    contact_person = models.CharField(max_length=100)
    relation = models.CharField(max_length=50)
    contact_address = models.CharField(max_length=255)
    passport_picture = models.ImageField(upload_to='passport_pictures/')

class EducationalBackground(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.CharField(max_length=50)
    school = models.CharField(max_length=100)
    date_started = models.DateField()
    date_completed = models.DateField()
    certificates = models.FileField(upload_to='certificates/', blank=True, null=True)

class ProfessionalRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    regulatory_body = models.CharField(max_length=100)
    registration_pin = models.CharField(max_length=50)
    date_received = models.DateField()

class MedicalHistory(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    physical_disability = models.BooleanField()
    disability_details = models.TextField(blank=True, null=True)
    medical_condition = models.BooleanField()
    condition_details = models.TextField(blank=True, null=True)

class PostingPreference(models.Model):
    REGION_CHOICES = [
        ('western', 'Western Region'),
        ('central', 'Central Region'),
        ('ashanti', 'Ashanti Region'),
        ('brong', 'Brong Ahafo Region'),
        ('upperWest', 'Upper West Region'),
        # Add more choices as needed
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_choice = models.CharField(max_length=20, choices=REGION_CHOICES, blank=True, null=True)
    second_choice = models.CharField(max_length=20, choices=REGION_CHOICES, blank=True, null=True)
    third_choice = models.CharField(max_length=20, choices=REGION_CHOICES, blank=True, null=True)
    fourth_choice = models.CharField(max_length=20, choices=REGION_CHOICES, blank=True, null=True)
    fifth_choice = models.CharField(max_length=20, choices=REGION_CHOICES, blank=True, null=True)

class MedicalCertification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    doctor_name = models.CharField(max_length=100)
    patient_name = models.CharField(max_length=100)
    position_applied_for = models.CharField(max_length=100)
    examination_date = models.DateField()
    chest_xray = models.CharField(max_length=255, blank=True, null=True)
    blood_pressure = models.CharField(max_length=50, blank=True, null=True)
    heart = models.CharField(max_length=255, blank=True, null=True)
    stool = models.CharField(max_length=255, blank=True, null=True)
    haemoglobin = models.CharField(max_length=50, blank=True, null=True)
    abdomen = models.CharField(max_length=255, blank=True, null=True)
    vision = models.CharField(max_length=255, blank=True, null=True)
    hearing = models.CharField(max_length=255, blank=True, null=True)
    lungs = models.CharField(max_length=255, blank=True, null=True)
    urine = models.CharField(max_length=255, blank=True, null=True)
    sickling = models.CharField(max_length=255, blank=True, null=True)
    extremities = models.CharField(max_length=255, blank=True, null=True)
    certification_status = models.CharField(max_length=255, choices=[('fit', 'Medically Fit'), ('fit_with_condition', 'Medically Fit with Condition'), ('unfit', 'Medically Unfit')])

class Addendum(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    license_cert = models.FileField(upload_to='license_cert/', blank=True, null=True)

class Declaration(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    agree = models.BooleanField()
    date = models.DateField()
    signature = models.CharField(max_length=100)

class Application(models.Model):
    personal_information = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE, default=1)
    educational_background = models.ForeignKey(EducationalBackground, on_delete=models.CASCADE, default=1)
    medical_history = models.ForeignKey(MedicalHistory, on_delete=models.CASCADE, default=1)
    posting_preference = models.ForeignKey(PostingPreference, on_delete=models.CASCADE, default=1)
    medical_certification = models.ForeignKey(MedicalCertification, on_delete=models.CASCADE,default=1)
    addendum = models.ForeignKey(Addendum, on_delete=models.CASCADE, default=1)  # Replace '1' with the ID of an existing Addendum
    declaration = models.ForeignKey(Declaration, on_delete=models.CASCADE, default=1)
    date_submitted = models.DateTimeField(auto_now_add=True)