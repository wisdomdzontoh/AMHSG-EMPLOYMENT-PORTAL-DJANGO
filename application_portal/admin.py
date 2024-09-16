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



@admin.register(PersonalInformation)
class PersonalInformationAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_title', 'title', 'email', 'first_name', 'surname', 'dob', 'telephone')
    search_fields = ('user__username', 'first_name', 'surname', 'email')
    list_filter = ('title', 'marital_status', 'gender')



class EducationalBackgroundAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'JHS_level', 'JHS_school', 'JHS_date_started', 'JHS_date_completed',
        'SHS_level', 'SHS_school', 'SHS_date_started', 'SHS_date_completed',
        'TERTIARY_level', 'TERTIARY_school', 'TERTIARY_date_started', 'TERTIARY_date_completed'
    )
    list_filter = ('JHS_level', 'SHS_level', 'TERTIARY_level')
    
admin.site.register(EducationalBackground, EducationalBackgroundAdmin)


@admin.register(ProfessionalRegistration)
class ProfessionalRegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'regulatory_body', 'license_cert', 'registration_pin', 'date_received')
    search_fields = ('user__username', 'regulatory_body')

@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'physical_disability', 'medical_condition')
    search_fields = ('user__username',)
    list_filter = ('physical_disability', 'medical_condition')






@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('region_name',)

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('facility_name', 'town_name', 'region')  # Ensure region exists in the Facility model
    list_filter = ('region',)  # Filter by region

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





@admin.register(MedicalCertification)
class MedicalCertificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'medical_cert')
    

@admin.register(Addendum)
class AddendumAdmin(admin.ModelAdmin):
    list_display = ('user', 'other_cert')
    search_fields = ('user__username',)

@admin.register(Declaration)
class DeclarationAdmin(admin.ModelAdmin):
    list_display = ('user', 'agree', 'date')
    search_fields = ('user__username',)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('personal_information', 'educational_background', 'medical_history', 'posting_preference', 'medical_certification', 'addendum', 'declaration', 'date_submitted')
    search_fields = ('personal_information_userusername', 'educational_backgrounduser_username')
    list_filter = ('date_submitted',)