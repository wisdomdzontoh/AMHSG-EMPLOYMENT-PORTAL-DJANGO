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
import logging
from django.db import IntegrityError
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from twilio.rest import Client
# Configure logging
logger = logging.getLogger(__name__)




@login_required(login_url="authentication:my-login")
def application_list(request):
    try:
        # Fetch all applications for the logged-in user, ordered by date in descending order
        applications = Application.objects.filter(
            personal_information__user=request.user
        ).order_by('-date_submitted')

        context = {
            'applications': applications
        }

        return render(request, 'application_portal/job_applications.html', context)

    except Exception as e:
        # Handle any exceptions and log errors if needed
        messages.error(request, "An error occurred while fetching applications.")
        return render(request, 'application_portal/job_applications.html', {'applications': None})



@login_required(login_url="authentication:my-login")
def faq(request):
    return render(request, 'application_portal/faq.html')




@login_required(login_url="authentication:my-login")
def application_portal(request):
    # Get the user's job applications
    job_applications = Application.objects.filter(user=request.user)

    # Prepare context data
    context = {
        'job_applications': job_applications,
        'number_of_jobs': job_applications.count(),
    }

    return render(request, 'application_portal/index.html', context)




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





# View for displaying applicant details in the admin panel
@staff_member_required
def admin_applicant_details(request, id):
    application = get_object_or_404(Application, pk=id)
    context = {
        'application': application,
    }
    return render(request, 'admin/application_portal/applicant_details.html', context)





from django.http import JsonResponse
from .models import Facility

def get_facilities(request, region_id):
    facilities = Facility.objects.filter(region_id=region_id).values('id', 'facility_name')
    return JsonResponse({'facilities': list(facilities)})





# Twilio Configuration
"""TWILIO_ACCOUNT_SID = 'AC1e777c6c07f78c6705c2aeb8d98c93e7'
TWILIO_AUTH_TOKEN = 'c5589da05e49f090752ba5f0d2f59009'
TWILIO_PHONE_NUMBER = '+233 55 874 9735'"""



#FORM SUBMISSION
@login_required(login_url="authentication:my-login")
@payment_required
def application_form(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    jobs = Job.objects.all()
    regions = Region.objects.all()
    
    # Fetch or create the user's personal information instance
    personal_info, created = PersonalInformation.objects.get_or_create(user=request.user)

    # Check if existing data exists for the user, except PostingPreference
    try:
        education = EducationalBackground.objects.get(user=request.user)
        registration = ProfessionalRegistration.objects.get(user=request.user)
        medical_history = MedicalHistory.objects.get(user=request.user)
        medical_certification = MedicalCertification.objects.get(user=request.user)
        addendum = Addendum.objects.get(user=request.user)
        declaration = Declaration.objects.get(user=request.user)
    except (EducationalBackground.DoesNotExist, ProfessionalRegistration.DoesNotExist,
            MedicalHistory.DoesNotExist, MedicalCertification.DoesNotExist, Addendum.DoesNotExist, Declaration.DoesNotExist):
        # Initialize to None if data doesn't exist
        education, registration, medical_history = None, None, None
        medical_certification, addendum, declaration = None, None, None

    if request.method == 'POST':
        # Instantiate forms with POST data and files
        personal_info_form = PersonalInformationForm(request.POST, request.FILES, instance=personal_info)
        education_form = EducationalBackgroundForm(request.POST, request.FILES, instance=education)
        registration_form = ProfessionalRegistrationForm(request.POST, request.FILES, instance=registration)
        medical_history_form = MedicalHistoryForm(request.POST, instance=medical_history)
        posting_preference_form = PostingPreferenceForm(request.POST)  # Always a new form
        medical_certification_form = MedicalCertificationForm(request.POST, request.FILES, instance=medical_certification)
        addendum_form = AddendumForm(request.POST, request.FILES, instance=addendum)
        declaration_form = DeclarationForm(request.POST, request.FILES, instance=declaration)

        if (personal_info_form.is_valid() and education_form.is_valid() and
            registration_form.is_valid() and medical_history_form.is_valid() and
            posting_preference_form.is_valid() and medical_certification_form.is_valid() and
            addendum_form.is_valid() and declaration_form.is_valid()):

            try:
                # Save or update personal info
                personal_info = personal_info_form.save(commit=False)
                personal_info.user = request.user
                #personal_info.job_title = job  # Update with current job
                if 'passport_picture' in request.FILES:
                    personal_info.passport_picture = request.FILES['passport_picture']
                personal_info.save()

                # Save or update other forms
                education = education_form.save(commit=False)
                education.user = request.user
                education.save()

                registration = registration_form.save(commit=False)
                registration.user = request.user
                registration.save()

                medical_history = medical_history_form.save(commit=False)
                medical_history.user = request.user
                medical_history.save()

                # Create a new PostingPreference each time with the current job
                posting_preference = posting_preference_form.save(commit=False)
                posting_preference.user = request.user
                posting_preference.job = job  # Link PostingPreference with the specific job
                posting_preference.save()

                medical_certification = medical_certification_form.save(commit=False)
                medical_certification.user = request.user
                medical_certification.save()

                addendum = addendum_form.save(commit=False)
                addendum.user = request.user
                addendum.save()

                declaration = declaration_form.save(commit=False)
                declaration.user = request.user
                declaration.save()

                # Handle file uploads explicitly if needed
                if 'other_cert' in request.FILES:
                    addendum.other_cert = request.FILES['other_cert']
                    addendum.save()

                # Create a new application for each job
                application, created = Application.objects.get_or_create(
                    personal_information=personal_info,
                    educational_background=education,
                    professional_registration=registration,
                    medical_history=medical_history,
                    posting_preference=posting_preference,  # Use new PostingPreference object here
                    medical_certification=medical_certification,
                    addendum=addendum,
                    declaration=declaration,
                    user=request.user,
                    job=job,
                    defaults={
                        'status': 'pending',
                        'date_submitted': timezone.now(),
                    }
                )

                messages.success(request, "Application submitted successfully! A confirmation SMS has been sent to your phone.")
                return redirect('application-success')

            except IntegrityError as e:
                logger.error(f"IntegrityError occurred: {str(e)}")
                messages.error(request, f"An error occurred: {str(e)}. Please contact support or try again.")
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
                    'jobs': jobs,
                    'regions': regions,
                })

    else:
        # Populate forms with existing data if available
        personal_info_form = PersonalInformationForm(instance=personal_info)
        education_form = EducationalBackgroundForm(instance=education)
        registration_form = ProfessionalRegistrationForm(instance=registration)
        medical_history_form = MedicalHistoryForm(instance=medical_history)
        posting_preference_form = PostingPreferenceForm()  # New form each time
        medical_certification_form = MedicalCertificationForm(instance=medical_certification)
        addendum_form = AddendumForm(instance=addendum)
        declaration_form = DeclarationForm(instance=declaration)

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
        'jobs': jobs,
        'regions': regions
    })






















