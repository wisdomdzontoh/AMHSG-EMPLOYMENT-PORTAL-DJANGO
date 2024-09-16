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
from .models import (
    PersonalInformation, EducationalBackground, ProfessionalRegistration, 
    MedicalHistory, PostingPreference, MedicalCertification, Declaration, Region, Facility
    )
from django.http import JsonResponse
from datetime import datetime
from .forms import (
    PersonalInformationForm, EducationalBackgroundForm, ProfessionalRegistrationForm,
    MedicalHistoryForm, PostingPreferenceForm, MedicalCertificationForm,
    AddendumForm, DeclarationForm
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






@login_required(login_url="authentication:my-login")
@payment_required
def application_form(request):
    regions = Region.objects.all()
    facilities_by_region = {}

    for region in regions:
        facilities = Facility.objects.filter(region=region)
        facilities_by_region[region.id] = list(facilities.values('id', 'facility_name'))

    user = request.user

    context = {
        'personal_info_form': PersonalInformationForm(instance=PersonalInformation.objects.filter(user=user).first() or None),
        'education_form': EducationalBackgroundForm(instance=EducationalBackground.objects.filter(user=user).first() or None),
        'professional_form': ProfessionalRegistrationForm(instance=ProfessionalRegistration.objects.filter(user=user).first() or None),
        'medical_history_form': MedicalHistoryForm(instance=MedicalHistory.objects.filter(user=user).first() or None),
        'posting_preference_form': PostingPreferenceForm(instance=PostingPreference.objects.filter(user=user).first() or None),
        'certification_form': MedicalCertificationForm(instance=MedicalCertification.objects.filter(user=user).first() or None),
        'addendum_form': AddendumForm(instance=Addendum.objects.filter(user=user).first() or None),
        'declaration_form': DeclarationForm(instance=Declaration.objects.filter(user=user).first() or None),
        'regions': regions,
        'facilities_by_region': facilities_by_region
    }

    if request.method == 'POST':
        section = request.POST.get('section')

        if not section:
            return JsonResponse({'success': False, 'message': 'Form section is missing. Please try again.'})

        form_class_mapping = {
            '1': PersonalInformationForm,
            '2': EducationalBackgroundForm,
            '3': ProfessionalRegistrationForm,
            '4': MedicalHistoryForm,
            '5': PostingPreferenceForm,
            '6': MedicalCertificationForm,
            '7': AddendumForm,
            '8': DeclarationForm,
        }

        model_class_mapping = {
            '1': PersonalInformation,
            '2': EducationalBackground,
            '3': ProfessionalRegistration,
            '4': MedicalHistory,
            '5': PostingPreference,
            '6': MedicalCertification,
            '7': Addendum, 
            '8': Declaration,
        }

        form_class = form_class_mapping.get(section)
        model_class = model_class_mapping.get(section)

        if not form_class or not model_class:
            return JsonResponse({'success': False, 'message': 'Invalid form section or model class.'})

        instance = model_class.objects.filter(user=user).first()
        form_instance = form_class(request.POST, request.FILES, instance=instance)
        form_instance.instance.user = user

        if form_instance.is_valid():
            form_instance.save()

            # Check if this is the last section
            if section == '8':
                personal_info = PersonalInformation.objects.filter(user=user).first()
                education = EducationalBackground.objects.filter(user=user).first()
                medical_history = MedicalHistory.objects.filter(user=user).first()
                posting_preference = PostingPreference.objects.filter(user=user).first()
                medical_certification = MedicalCertification.objects.filter(user=user).first()
                addendum = Addendum.objects.filter(user=user).first()
                declaration = Declaration.objects.filter(user=user).first()

                # Ensure all sections are completed
                if all([personal_info, education, medical_history, posting_preference, medical_certification, addendum, declaration]):
                    Application.objects.create(
                        personal_information=personal_info,
                        educational_background=education,
                        medical_history=medical_history,
                        posting_preference=posting_preference,
                        medical_certification=medical_certification,
                        addendum=addendum,
                        declaration=declaration,
                    )
                    messages.success(request, 'Application submitted successfully!')
                    return redirect('application-success')
                else:
                    return JsonResponse({'success': False, 'message': 'Some form sections are missing or incomplete.'})

            # Proceed to the next section
            next_section = int(section) + 1 if section != '8' else None
            return JsonResponse({'success': True, 'next_section': next_section, 'message': f'Section {section} saved successfully!'})

        else:
            return JsonResponse({'success': False, 'message': form_instance.errors})

    return render(request, 'application_portal/application-form.html', context)



