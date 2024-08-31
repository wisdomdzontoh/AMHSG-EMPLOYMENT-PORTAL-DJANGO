from django.contrib import admin
from .models import (
    PersonalInformation,
    EducationalBackground,
    ProfessionalRegistration,
    MedicalHistory,
    PostingPreference,
    MedicalCertification,
    Addendum,
    Declaration,
    Application
)

@admin.register(PersonalInformation)
class PersonalInformationAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_title', 'title', 'email', 'first_name', 'surname', 'dob', 'telephone')
    search_fields = ('user__username', 'first_name', 'surname', 'email')
    list_filter = ('title', 'marital_status', 'gender')

@admin.register(EducationalBackground)
class EducationalBackgroundAdmin(admin.ModelAdmin):
    list_display = ('user', 'level', 'school', 'date_started', 'date_completed')
    search_fields = ('user__username', 'school')
    list_filter = ('level',)

@admin.register(ProfessionalRegistration)
class ProfessionalRegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'regulatory_body', 'registration_pin', 'date_received')
    search_fields = ('user__username', 'regulatory_body')

@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'physical_disability', 'medical_condition')
    search_fields = ('user__username',)
    list_filter = ('physical_disability', 'medical_condition')

@admin.register(PostingPreference)
class PostingPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_choice', 'second_choice', 'third_choice', 'fourth_choice', 'fifth_choice')
    search_fields = ('user__username',)
    list_filter = ('first_choice', 'second_choice', 'third_choice', 'fourth_choice', 'fifth_choice')

@admin.register(MedicalCertification)
class MedicalCertificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'doctor_name', 'patient_name', 'examination_date', 'certification_status')
    search_fields = ('user__username', 'doctor_name', 'patient_name')
    list_filter = ('certification_status',)

@admin.register(Addendum)
class AddendumAdmin(admin.ModelAdmin):
    list_display = ('user', 'license_cert')
    search_fields = ('user__username',)

@admin.register(Declaration)
class DeclarationAdmin(admin.ModelAdmin):
    list_display = ('user', 'agree', 'date')
    search_fields = ('user__username',)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('personal_information', 'educational_background', 'medical_history', 'posting_preference', 'medical_certification', 'addendum', 'declaration', 'date_submitted')
    search_fields = ('personal_information__user__username', 'educational_background__user__username')
    list_filter = ('date_submitted',)
