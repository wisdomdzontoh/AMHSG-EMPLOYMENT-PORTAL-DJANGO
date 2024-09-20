from django import forms
from .models import (
    PersonalInformation, EducationalBackground, ProfessionalRegistration,
    MedicalHistory, PostingPreference, MedicalCertification, Addendum, Declaration, Region, Facility
)
from django.core.exceptions import ValidationError
from django.core.exceptions import ValidationError






class PersonalInformationForm(forms.ModelForm):
    class Meta:
        model = PersonalInformation
        fields = [
            'title', 'email', 'first_name', 'surname', 'other_names',
            'dob', 'telephone', 'ghana_card_number', 'birthplace', 'marital_status', 'gender', 'fathers_name',
            'fathers_occupation', 'mothers_name', 'mothers_occupation', 'next_of_kin',
            'next_of_kin_occupation', 'contact_person', 'relation', 'contact_address', 
            'passport_picture'
        ]
        widgets = {'dob': forms.DateInput(attrs={'type': 'date'})}

class EducationalBackgroundForm(forms.ModelForm):
    class Meta:
        model = EducationalBackground
        fields = ['JHS_level', 'JHS_school', 'JHS_date_started', 'JHS_date_completed', 'JHS_field_of_study', 'JHS_certificates', 
                  'SHS_level', 'SHS_school', 'SHS_date_started', 'SHS_date_completed', 'SHS_field_of_study', 'SHS_certificates',
                  'TERTIARY_level', 'TERTIARY_school', 'TERTIARY_date_started', 'TERTIARY_date_completed', 'TERTIARY_field_of_study', 'TERTIARY_certificates',]
        widgets = {'JHS_date_started': forms.DateInput(attrs={'type': 'date'}),'JHS_date_completed': forms.DateInput(attrs={'type': 'date'}),'SHS_date_started': forms.DateInput(attrs={'type': 'date'}), 'SHS_date_completed': forms.DateInput(attrs={'type': 'date'}), 'TERTIARY_date_started': forms.DateInput(attrs={'type': 'date'}), 'TERTIARY_date_completed': forms.DateInput(attrs={'type': 'date'})}

class ProfessionalRegistrationForm(forms.ModelForm):
    class Meta:
        model = ProfessionalRegistration
        fields = ['regulatory_body', 'registration_pin', 'date_received', 'license_cert']
        widgets = {'date_received': forms.DateInput(attrs={'type': 'date'})}

class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = ['physical_disability', 'disability_details', 'medical_condition', 'condition_details']







class PostingPreferenceForm(forms.ModelForm):
    class Meta:
        model = PostingPreference
        fields = [
            'first_choice_region', 'first_choice_facility', 
            'second_choice_region', 'second_choice_facility', 
            'third_choice_region', 'third_choice_facility'
        ]
        widgets = {
            'first_choice_region': forms.Select(attrs={'id': 'first_choice_region'}),
            'first_choice_facility': forms.Select(attrs={'id': 'first_choice_facility'}),
            'second_choice_region': forms.Select(attrs={'id': 'second_choice_region'}),
            'second_choice_facility': forms.Select(attrs={'id': 'second_choice_facility'}),
            'third_choice_region': forms.Select(attrs={'id': 'third_choice_region'}),
            'third_choice_facility': forms.Select(attrs={'id': 'third_choice_facility'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        first_choice_region = cleaned_data.get('first_choice_region')
        first_choice_facility = cleaned_data.get('first_choice_facility')
        second_choice_region = cleaned_data.get('second_choice_region')
        second_choice_facility = cleaned_data.get('second_choice_facility')
        third_choice_region = cleaned_data.get('third_choice_region')
        third_choice_facility = cleaned_data.get('third_choice_facility')

        # Check for duplicate region selections
        if first_choice_region and second_choice_region and first_choice_region == second_choice_region:
            raise ValidationError("You cannot select the same region for first and second choices.")
        if first_choice_region and third_choice_region and first_choice_region == third_choice_region:
            raise ValidationError("You cannot select the same region for first and third choices.")
        if second_choice_region and third_choice_region and second_choice_region == third_choice_region:
            raise ValidationError("You cannot select the same region for second and third choices.")

        # Check for duplicate facility selections
        if first_choice_facility and second_choice_facility and first_choice_facility == second_choice_facility:
            raise ValidationError("You cannot select the same facility for first and second choices.")
        if first_choice_facility and third_choice_facility and first_choice_facility == third_choice_facility:
            raise ValidationError("You cannot select the same facility for first and third choices.")
        if second_choice_facility and third_choice_facility and second_choice_facility == third_choice_facility:
            raise ValidationError("You cannot select the same facility for second and third choices.")

        return cleaned_data


    


class MedicalCertificationForm(forms.ModelForm):
    class Meta:
        model = MedicalCertification
        fields = [
            'medical_cert'
        ]
        

class AddendumForm(forms.ModelForm):
    class Meta:
        model = Addendum
        fields = ['other_cert']

class DeclarationForm(forms.ModelForm):
    class Meta:
        model = Declaration
        fields = ['agree', 'date', 'signature']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}