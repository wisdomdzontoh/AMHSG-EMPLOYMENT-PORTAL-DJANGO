from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Application
from payment.models import Voucher
from payment.decorators import payment_required
import random
import string
from .models import PersonalInformation, EducationalBackground, ProfessionalRegistration, MedicalHistory, PostingPreference, MedicalCertification, Declaration
from django.http import JsonResponse
from datetime import datetime


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
@payment_required
def application_form(request):
    user = request.user

    if request.method == 'POST':
        section = request.POST.get('section')

        if not section:
            # Return error if section is not provided
            return JsonResponse({'success': False, 'message': 'Form section is missing. Please try again.'})

        try:
            if section == '1':
                # Save Personal Information
                personal_info, created = PersonalInformation.objects.get_or_create(user=user)
                personal_info.title = request.POST.get('title')
                personal_info.email = request.POST.get('email')
                personal_info.first_name = request.POST.get('first_name')
                personal_info.surname = request.POST.get('surname')
                personal_info.other_names = request.POST.get('other_names')
                personal_info.dob = request.POST.get('dob')
                dob_str = request.POST.get('dob')  # Get the dob field from the form
                if dob_str:
                    try:
                        # Validate and parse the date
                        personal_info.dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
                    except ValueError:
                        return JsonResponse({'success': False, 'message': 'Invalid date format. Please use YYYY-MM-DD.'})
                else:
                    return JsonResponse({'success': False, 'message': 'Date of Birth is required.'})
                personal_info.telephone = request.POST.get('telephone')
                personal_info.birthplace = request.POST.get('birthplace')
                personal_info.marital_status = request.POST.get('marital_status')
                personal_info.gender = request.POST.get('gender')
                personal_info.fathers_name = request.POST.get('fathers_name')
                personal_info.fathers_occupation = request.POST.get('fathers_occupation')
                personal_info.mothers_name = request.POST.get('mothers_name')
                personal_info.mothers_occupation = request.POST.get('mothers_occupation')
                personal_info.next_of_kin = request.POST.get('next_of_kin')
                personal_info.next_of_kin_occupation = request.POST.get('next_of_kin_occupation')
                personal_info.contact_person = request.POST.get('contact_person')
                personal_info.relation = request.POST.get('relation')
                personal_info.contact_address = request.POST.get('contact_address')
                
                if 'passport_picture' in request.FILES:
                    personal_info.passport_picture = request.FILES['passport_picture']
                personal_info.save()

                return JsonResponse({'success': True, 'message': 'Personal Information saved successfully!'})

            elif section == '2':
                # Save Educational Background
                education = EducationalBackground(user=user)
                education.level = request.POST.get('level')
                education.school = request.POST.get('school')
                education.date_started = request.POST.get('date_started')
                education.date_completed = request.POST.get('date_completed')
                if 'certificates' in request.FILES:
                    education.certificates = request.FILES['certificates']
                education.save()

                return JsonResponse({'success': True, 'message': 'Educational Background saved successfully!'})

            # Add logic for other sections (3 to 8)

            # Handle the "Next" button click by returning the next section number
            next_section = int(section) + 1
            return JsonResponse({'success': True, 'next_section': next_section, 'message': f'Section {section} saved successfully!'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})

    # Render the form template for the initial load
    return render(request, 'application_portal/application-form.html')

