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
    Application,
    Region,
    Facility
)
import openpyxl
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
import io
import os
from django.conf import settings
from PyPDF2 import PdfMerger
# Register Application Admin with export functionalities
from django.contrib import admin
from .models import Application
from .actions import export_as_excel, export_application_as_pdf

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = (
        'personal_information', 
        'educational_background', 
        'medical_history', 
        'professional_registration',
        'posting_preference', 
        'medical_certification', 
        'addendum', 
        'declaration', 
        'date_submitted'
    )
    search_fields = (
        'personal_information__user__username',  # Searching by username in personal information
        'personal_information__application_id',  # Searching by application ID
    )
    list_filter = ('date_submitted',)  # Filter by submission date
    actions = [export_as_excel, export_application_as_pdf]  # Actions for export



# For Personal Information Admin
@admin.register(PersonalInformation)
class PersonalInformationAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'email', 'first_name', 'surname', 'dob', 'telephone')
    search_fields = ('user__username', 'first_name', 'surname', 'email', 'ghana_card_number')
    list_filter = ('title', 'marital_status', 'gender')


# Educational Background Admin
class EducationalBackgroundAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'JHS_level', 'JHS_school', 'JHS_date_started', 'JHS_date_completed',
        'SHS_level', 'SHS_school', 'SHS_date_started', 'SHS_date_completed',
        'TERTIARY_level', 'TERTIARY_school', 'TERTIARY_date_started', 'TERTIARY_date_completed'
    )
    list_filter = ('JHS_level', 'SHS_level', 'TERTIARY_level')

admin.site.register(EducationalBackground, EducationalBackgroundAdmin)


# Professional Registration Admin
@admin.register(ProfessionalRegistration)
class ProfessionalRegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'regulatory_body', 'license_cert', 'registration_pin', 'date_received')
    search_fields = ('user__username', 'regulatory_body')


# Medical History Admin
@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'physical_disability', 'medical_condition')
    search_fields = ('user__username',)
    list_filter = ('physical_disability', 'medical_condition')


# Region Admin
@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('region_name',)


# Facility Admin
@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('facility_name', 'town_name', 'region')
    list_filter = ('region',)


# Posting Preference Admin
@admin.register(PostingPreference)
class PostingPreferenceAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'first_choice_region', 'first_choice_facility',
        'second_choice_region', 'second_choice_facility',
        'third_choice_region', 'third_choice_facility',
    )
    list_filter = (
        'first_choice_region', 'first_choice_facility',
        'second_choice_region', 'second_choice_facility',
        'third_choice_region', 'third_choice_facility',
    )


# Medical Certification Admin
@admin.register(MedicalCertification)
class MedicalCertificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'medical_cert')


# Addendum Admin
@admin.register(Addendum)
class AddendumAdmin(admin.ModelAdmin):
    list_display = ('user', 'other_cert')
    search_fields = ('user__username',)


# Declaration Admin
@admin.register(Declaration)
class DeclarationAdmin(admin.ModelAdmin):
    list_display = ('user', 'agree', 'date')
    search_fields = ('user__username',)
    list_filter = ('agree', 'date')
