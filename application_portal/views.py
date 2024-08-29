from .models import Application
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from payment.models import Voucher
import random
import string
from payment.decorators import payment_required

@login_required(login_url="my-login")
def application_list(request):
    # Fetch all applications and order them by date in descending order
    applications = Application.objects.all().order_by('-date')
    
    # Prepare context with applications to pass to the template
    context = {
        'applications': applications.filter(user=request.user)
    }
    
    # Render the template with the context
    return render(request, 'application_portal/job_applications.html', context)


@login_required(login_url="my-login")
def application_portal(request):
    return render(request, 'application_portal/index.html')




@login_required
def purchase_voucher(request):
    if request.method == 'POST':
        # Process payment (You would integrate with a payment gateway here)
        
        # After payment is successful
        user = request.user
        voucher_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        pin = ''.join(random.choices(string.digits, k=6))

        voucher = Voucher.objects.create(
            user=user,
            voucher_code=voucher_code,
            pin=pin
        )

        # Redirect to a success page or the My Application page
        return redirect('voucher_success', voucher_id=voucher.id)

    return render(request, 'application_portal/index.html')





@login_required(login_url='login')  # Ensures only logged-in users can access the view
@payment_required  # Checks if the user has made a verified payment
def application_form(request):
    # Your application form logic here
    return render(request, 'application_portal/application-form.html')


