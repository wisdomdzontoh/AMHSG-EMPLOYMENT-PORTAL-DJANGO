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


# Excel Export Functionality
def export_as_excel(modeladmin, request, queryset):
    # Create an in-memory workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Applications"

    # Write header row
    headers = [
        "User", "Job Title", "Title", "First Name", "Surname", "Email", "DOB", "Telephone",
        "JHS Level", "SHS Level", "TERTIARY Level", "Regulatory Body", "Registration PIN", "Date Received",
        "Physical Disability", "Medical Condition", "First Choice Region", "First Choice Facility",
        "Second Choice Region", "Second Choice Facility", "Third Choice Region", "Third Choice Facility",
        "Medical Certificate", "Other Certificates", "Declaration Date", "Date Submitted"
    ]
    ws.append(headers)

    # Write data rows
    for obj in queryset:
        # Personal Information
        personal_info = obj.personal_information
        educational_background = obj.educational_background
        professional_registration = obj.professional_registration
        medical_history = obj.medical_history
        posting_preference = obj.posting_preference
        medical_cert = obj.medical_certification.medical_cert.url if obj.medical_certification.medical_cert else 'N/A'
        addendum = obj.addendum.other_cert.url if obj.addendum.other_cert else 'N/A'
        declaration = obj.declaration.date.strftime('%Y-%m-%d') if obj.declaration else 'N/A'
        date_submitted = obj.date_submitted.strftime('%Y-%m-%d')

        # Prepare a row of data
        row = [
            personal_info.user.username,
            str(personal_info.job_title) if personal_info.job_title else 'N/A',  # Convert Job ForeignKey to string
            personal_info.title,
            personal_info.first_name,
            personal_info.surname,
            personal_info.email,
            personal_info.dob.strftime('%Y-%m-%d'),
            personal_info.telephone,

            # Educational Background
            educational_background.JHS_level,
            educational_background.SHS_level,
            educational_background.TERTIARY_level,

            # Professional Registration
            professional_registration.regulatory_body,
            professional_registration.registration_pin,
            professional_registration.date_received.strftime('%Y-%m-%d'),

            # Medical History
            "Yes" if medical_history.physical_disability else "No",
            "Yes" if medical_history.medical_condition else "No",

            # Posting Preferences
            posting_preference.first_choice_region.region_name if posting_preference.first_choice_region else 'N/A',
            posting_preference.first_choice_facility.facility_name if posting_preference.first_choice_facility else 'N/A',
            posting_preference.second_choice_region.region_name if posting_preference.second_choice_region else 'N/A',
            posting_preference.second_choice_facility.facility_name if posting_preference.second_choice_facility else 'N/A',
            posting_preference.third_choice_region.region_name if posting_preference.third_choice_region else 'N/A',
            posting_preference.third_choice_facility.facility_name if posting_preference.third_choice_facility else 'N/A',

            # Medical Certificate and Other Documents
            medical_cert,
            addendum,

            # Declaration and Date Submitted
            declaration,
            date_submitted
        ]
        ws.append(row)

    # Create HTTP response with the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=applications.xlsx'
    wb.save(response)
    return response

export_as_excel.short_description = "Export selected applications to Excel"


# PDF Export Functionality
def export_application_as_pdf(modeladmin, request, queryset):
    for obj in queryset:
        # Render the HTML template for the application as a string
        html_string = render_to_string('application_portal/applicant_details.html', {'application': obj})
        
        # Create an HttpResponse object with the correct PDF headers
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="application_{obj.personal_information.user.username}.pdf"'
        
        # Convert the HTML string to a PDF using xhtml2pdf (pisa)
        pisa_status = pisa.CreatePDF(html_string, dest=response)
        
        # If there was an error, show it in the response
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html_string + '</pre>')
        return response

export_application_as_pdf.short_description = "Download selected applications as PDF"


# Register Application Admin with export functionalities
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('personal_information', 'educational_background', 'medical_history', 'posting_preference', 'medical_certification', 'addendum', 'declaration', 'date_submitted')
    search_fields = ('personal_information__user__username', 'educational_background__user__username')
    list_filter = ('date_submitted',)
    actions = [export_as_excel, export_application_as_pdf]  # Added PDF export action


# For Personal Information Admin
@admin.register(PersonalInformation)
class PersonalInformationAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_title', 'title', 'email', 'first_name', 'surname', 'dob', 'telephone')
    search_fields = ('user__username', 'first_name', 'surname', 'email', 'ghana_card_number')
    list_filter = ('title', 'marital_status', 'gender', 'job_title')


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
