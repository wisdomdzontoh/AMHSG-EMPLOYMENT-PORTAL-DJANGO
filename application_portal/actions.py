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



# Excel Export Functionality
def export_as_excel(modeladmin, request, queryset):
    # Create an in-memory workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Applications"

    # Write header row
    headers = [
        "User", "Title", "First Name", "Surname", "Email", "DOB", "Telephone", "GH Card Number", 
        "Gender", "Fathers Name", "Fathers Occupation", "Mothers Name", "Mothers Occupation", "Next of Kin", "Next of Kin Occupation", "Contact Person", "Relation", "Contact Address", "Passport Picture",
        "JHS Level", "JHS school", "JHS Field of study", "JHS Date Started", "JSH Date Completed",
        "SHS Level", "SHS School", "SHS field of study", "shs Date started", "SHS Date Completed",
        "TERTIARY Level", "TERTIARY School", "TERTIARY field of study", "TERTIARY Date started", "TERTIARY Date completed", 
        "Regulatory Body", "Registration PIN", "Date Received",
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
            personal_info.title,
            personal_info.first_name,
            personal_info.surname,
            personal_info.email,
            personal_info.dob.strftime('%Y-%m-%d'),
            personal_info.telephone,
            personal_info.ghana_card_number,
            personal_info.gender,
            personal_info.fathers_name,
            personal_info.fathers_occupation,
            personal_info.mothers_name,
            personal_info.mothers_occupation,
            personal_info.next_of_kin,
            personal_info.next_of_kin_occupation,
            personal_info.contact_person,
            personal_info.relation,
            personal_info.contact_address,
            "Yes" if personal_info.passport_picture else "No",
            
            # Educational Background
            educational_background.JHS_level,
            educational_background.JHS_school,
            educational_background.JHS_field_of_study,
            educational_background.JHS_date_started,
            educational_background.JHS_date_completed,
            
            educational_background.SHS_level,
            educational_background.SHS_school,
            educational_background.SHS_field_of_study,
            educational_background.SHS_date_started,
            educational_background.SHS_date_completed,
            
            educational_background.TERTIARY_level,
            educational_background.TERTIARY_school,
            educational_background.TERTIARY_field_of_study,
            educational_background.TERTIARY_date_started,
            educational_background.TERTIARY_date_completed,
            
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
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="applications.pdf"'
    
    # Create the PDF for each selected object
    pdfs = []
    for obj in queryset:
        # Pass the absolute file paths to your template
        html_string = render_to_string('application_portal/applicant_details.html', {
            'application': obj,
            'STATIC_ROOT': settings.STATIC_ROOT,  # Pass static root to access static files correctly
            'MEDIA_ROOT': settings.MEDIA_ROOT,    # Pass media root to access media files correctly
        })
        
        result = io.BytesIO()
        pdf = pisa.CreatePDF(io.StringIO(html_string), dest=result)
        
        if pdf.err:
            return HttpResponse(f'We had some errors while creating the PDF: <pre>{html_string}</pre>')
        
        pdfs.append(result.getvalue())
    
    # Merge PDFs and write to response
    merger = PdfMerger()
    for pdf in pdfs:
        merger.append(io.BytesIO(pdf))
    
    merger.write(response)
    merger.close()
    
    return response