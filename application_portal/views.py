import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Addendum, Application
from payment.models import Voucher
from payment.decorators import payment_required
from django.urls import reverse
import random
import string
from django.http import JsonResponse
from datetime import datetime
from django.db import IntegrityError
from django.utils import timezone  # Import timezone
from django.db import IntegrityError
from .forms import (
    PersonalInformationForm, EducationalBackgroundForm, ProfessionalRegistrationForm,
    MedicalHistoryForm, PostingPreferenceForm, MedicalCertificationForm, AddendumForm, DeclarationForm
)
from .models import (
    Application, PersonalInformation, EducationalBackground, ProfessionalRegistration,
    MedicalHistory, PostingPreference, MedicalCertification, Addendum, Job, Declaration, Region, Facility
)





@login_required(login_url="authentication:my-login")
def application_list(request):
    # Fetch all applications for the logged-in user, ordered by date in descending order
    applications = Application.objects.filter(personal_information__user=request.user).order_by('-date_submitted')
    
    context = {
        'applications': applications
    }
    
    return render(request, 'application_portal/job_applications.html', context)




@login_required(login_url="authentication:my-login")
def application_portal(request):
    return render(request, 'application_portal/index.html')




@login_required(login_url="authentication:my-login")
def purchase_voucher(request):
    if request.method == 'POST':
        # Simulate payment processing logic
        # After payment is successful
        user = request.user
        voucher_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        pin = ''.join(random.choices(string.digits, k=6))

        voucher = Voucher.objects.create(
            user=user,
            voucher_code=voucher_code,
            pin=pin
        )

        # Redirect to a success page or display a success message
        messages.success(request, "Voucher purchased successfully!")
        return redirect('voucher_success', voucher_id=voucher.id)

    return render(request, 'application_portal/purchase_voucher.html')




@login_required(login_url="authentication:my-login")
def application_success(request):
    """
    Renders a success page after the application is successfully submitted.
    """
    return render(request, 'application_portal/application_success.html')






from django.http import JsonResponse
from .models import Facility

def get_facilities(request, region_id):
    facilities = Facility.objects.filter(region_id=region_id).values('id', 'facility_name')
    return JsonResponse({'facilities': list(facilities)})






@login_required(login_url="authentication:my-login")
@payment_required
def application_form(request, job_id):
    # Fetch the job using job_id
    job = get_object_or_404(Job, id=job_id)
    jobs = Job.objects.all()
    regions = Region.objects.all()

    if request.method == 'POST':
        # Instantiate forms with POST data and files
        personal_info_form = PersonalInformationForm(request.POST, request.FILES)
        education_form = EducationalBackgroundForm(request.POST, request.FILES)
        registration_form = ProfessionalRegistrationForm(request.POST, request.FILES)
        medical_history_form = MedicalHistoryForm(request.POST)
        posting_preference_form = PostingPreferenceForm(request.POST)
        medical_certification_form = MedicalCertificationForm(request.POST, request.FILES)
        addendum_form = AddendumForm(request.POST, request.FILES)
        declaration_form = DeclarationForm(request.POST, request.FILES)

        # Validate each form
        if (personal_info_form.is_valid() and education_form.is_valid() and
                registration_form.is_valid() and medical_history_form.is_valid() and
                posting_preference_form.is_valid() and medical_certification_form.is_valid() and
                addendum_form.is_valid() and declaration_form.is_valid()):
            
            try:
                # Create or update each form's corresponding model (user-specific)
                personal_info, _ = PersonalInformation.objects.get_or_create(
                    user=request.user,
                    defaults=personal_info_form.cleaned_data
                )

                education, _ = EducationalBackground.objects.get_or_create(
                    user=request.user,
                    defaults=education_form.cleaned_data
                )

                registration, _ = ProfessionalRegistration.objects.get_or_create(
                    user=request.user,
                    defaults=registration_form.cleaned_data
                )

                medical_history, _ = MedicalHistory.objects.get_or_create(
                    user=request.user,
                    defaults=medical_history_form.cleaned_data
                )

                posting_preference, _ = PostingPreference.objects.get_or_create(
                    user=request.user,
                    defaults=posting_preference_form.cleaned_data
                )

                medical_certification, _ = MedicalCertification.objects.get_or_create(
                    user=request.user,
                    defaults=medical_certification_form.cleaned_data
                )

                addendum, _ = Addendum.objects.get_or_create(
                    user=request.user,
                    defaults=addendum_form.cleaned_data
                )

                declaration, _ = Declaration.objects.get_or_create(
                    user=request.user,
                    defaults=declaration_form.cleaned_data
                )

                # Create or update application for the job (add job and user as part of uniqueness)
                application, _ = Application.objects.get_or_create(
                    personal_information=personal_info,
                    educational_background=education,
                    medical_history=medical_history,
                    posting_preference=posting_preference,
                    medical_certification=medical_certification,
                    addendum=addendum,
                    declaration=declaration,
                    user=request.user,  # Added user to make application specific to a user
                    job=job,  # Ensure job is included in the uniqueness check
                    defaults={
                        'status': 'pending',
                        'date_submitted': timezone.now(),
                    }
                )

                return redirect('application-success')  # Redirect on success

            except IntegrityError:
                # Handle form save errors
                return render(request, 'application_portal/application-form.html', {
                    'personal_info_form': personal_info_form,
                    'education_form': education_form,
                    'registration_form': registration_form,
                    'medical_history_form': medical_history_form,
                    'posting_preference_form': posting_preference_form,
                    'medical_certification_form': medical_certification_form,
                    'addendum_form': addendum_form,
                    'declaration_form': declaration_form,
                    'job': job,
                    'error': 'An error occurred while saving your data. Please try again.'
                })

    else:
        # Instantiate empty forms for GET request
        personal_info_form = PersonalInformationForm()
        education_form = EducationalBackgroundForm()
        registration_form = ProfessionalRegistrationForm()
        medical_history_form = MedicalHistoryForm()
        posting_preference_form = PostingPreferenceForm()
        medical_certification_form = MedicalCertificationForm()
        addendum_form = AddendumForm()
        declaration_form = DeclarationForm()

    return render(request, 'application_portal/application-form.html', {
        'personal_info_form': personal_info_form,
        'education_form': education_form,
        'registration_form': registration_form,
        'medical_history_form': medical_history_form,
        'posting_preference_form': posting_preference_form,
        'medical_certification_form': medical_certification_form,
        'addendum_form': addendum_form,
        'declaration_form': declaration_form,
        'job': job,  # Pass the job to the template so its ID can be used
        'jobs': jobs,
        'regions': regions  # Pass the regions to the template for dropdown options
    })















