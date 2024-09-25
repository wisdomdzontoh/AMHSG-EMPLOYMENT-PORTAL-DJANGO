from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.http import HttpResponse
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
from .actions import export_as_excel, export_application_as_pdf


# Application Admin with export functionalities
from django.utils.html import format_html
from django.urls import reverse

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
        'date_submitted',
        'application_id',
        'view_details_link',  # Add custom view details link
    )
    search_fields = (
        'personal_information__user__username',
        'application_id',
    )
    list_filter = ('date_submitted', 'job')
    actions = [export_as_excel, export_application_as_pdf]

    # Add the custom URL for application details
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:id>/details/', self.admin_site.admin_view(self.admin_applicant_details), name='admin_applicant_details'),
        ]
        return custom_urls + urls

    # The view handling the custom admin URL
    def admin_applicant_details(self, request, id):
        application = get_object_or_404(Application, pk=id)
        context = {
            'application': application,
        }
        return TemplateResponse(request, 'application_portal/applicant_details.html', context)

    # Custom method for the "View Details" link
    def view_details_link(self, obj):
        url = reverse('admin:admin_applicant_details', args=[obj.id])
        return format_html('<a href="{}">View Details</a>', url)

    view_details_link.short_description = "Details"



# Personal Information Admin
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
