from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Application
from payment.models import Voucher
from payment.decorators import payment_required
import random
import string

@login_required(login_url="my-login")
def application_list(request):
    # Fetch all applications for the logged-in user, ordered by date in descending order
    applications = Application.objects.filter(personal_information__user=request.user).order_by('-date_submitted')
    
    context = {
        'applications': applications
    }
    
    return render(request, 'application_portal/job_applications.html', context)

@login_required(login_url="my-login")
def application_portal(request):
    return render(request, 'application_portal/index.html')

@login_required(login_url='login') 
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

@login_required(login_url='login')  # Ensures only logged-in users can access the view
@payment_required  # Checks if the user has made a verified payment
def application_form(request):
    if request.method == 'POST':
        # Handle form submission and data saving logic for application form
        # Process different sections of the form and save them step-by-step
        # You might use `request.POST` to capture form data

        messages.success(request, "Application form submitted successfully!")
        return redirect('application_portal')  # Redirect to a confirmation or success page

    # Render the form template if it's a GET request
    return render(request, 'application_portal/application-form.html')
