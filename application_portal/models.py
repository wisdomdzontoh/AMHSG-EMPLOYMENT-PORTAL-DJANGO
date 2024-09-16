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
    JHS_level = models.CharField(max_length=50, default="none")
    JHS_school = models.CharField(max_length=100, default="none")
    JHS_field_of_study = models.CharField(max_length=100, default="none")
    JHS_date_started = models.DateField(default=timezone.now)
    JHS_date_completed = models.DateField(default=timezone.now)
    JHS_certificates = models.FileField(upload_to='certificates/JHS/', blank=True, null=True)
    
    SHS_level = models.CharField(max_length=50, default="none")
    SHS_school = models.CharField(max_length=100, default="none")
    SHS_field_of_study = models.CharField(max_length=100, default="none")
    SHS_date_started = models.DateField(default=timezone.now)
    SHS_date_completed = models.DateField(default=timezone.now)
    SHS_certificates = models.FileField(upload_to='certificates/SHS/', blank=True, null=True)
    
    
    TERTIARY_level = models.CharField(max_length=50, default="none")
    TERTIARY_school = models.CharField(max_length=100, default="none")
    TERTIARY_field_of_study = models.CharField(max_length=100, default="none")
    TERTIARY_date_started = models.DateField(default=timezone.now)
    TERTIARY_date_completed = models.DateField(default=timezone.now)
    TERTIARY_certificates = models.FileField(upload_to='certificates/TERTIARY/', blank=True, null=True)


class ProfessionalRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    regulatory_body = models.CharField(max_length=100)
    registration_pin = models.CharField(max_length=50)
    date_received = models.DateField()
    license_cert = models.FileField(upload_to='license_cert/', blank=True, null=True)
    

class MedicalHistory(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    physical_disability = models.BooleanField()
    disability_details = models.TextField(blank=True, null=True)
    medical_condition = models.BooleanField()
    condition_details = models.TextField(blank=True, null=True)

class Region(models.Model):
    region_name = models.CharField(max_length=50, default="none")
    
    def __str__(self):
        return self.region_name

class Facility(models.Model):
    facility_name = models.CharField(max_length=50, default="none")
    town_name = models.CharField(max_length=50, default="none")
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='facilities')  # Add this field

    def __str__(self):
        return f"{self.facility_name} - {self.town_name}"


class PostingPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # First choice of region and facility
    first_choice_region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="first_choice_region", null=True, blank=True)
    first_choice_facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="first_choice_facility", null=True, blank=True)

    # Second choice of region and facility
    second_choice_region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="second_choice_region", null=True, blank=True)
    second_choice_facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="second_choice_facility", null=True, blank=True)

    # Third choice of region and facility
    third_choice_region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="third_choice_region", null=True, blank=True)
    third_choice_facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name="third_choice_facility", null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Posting Preferences"



class MedicalCertification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    medical_cert = models.FileField(upload_to='medical_cert/', blank=True, null=True)
    

class Addendum(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    other_cert = models.FileField(upload_to='other_cert/', blank=True, null=True)

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
    status = models.CharField(max_length=50, default="pending")
    date_submitted = models.DateTimeField(auto_now_add=True)