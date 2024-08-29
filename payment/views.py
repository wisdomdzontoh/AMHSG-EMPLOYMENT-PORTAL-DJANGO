from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Payment  # Assuming you have a Payment model
from django.contrib.auth.models import User
from django.conf import settings
from application_portal import urls, views
from django.contrib import messages
from application_portal import views, urls



def initiate_payment(request: HttpRequest) -> HttpResponse:
    
    if request.method == "POST":
        # Capture the form data from the POST request
        amount = request.POST.get('amount')
        phone_number = request.POST.get('phone_number')
        user = request.user.username
        ref = request.POST.get('ref')
        
        
        # Perform any necessary validation here
        if amount and phone_number and ref and ref:
            # Save the payment details to the database
            payment = Payment.objects.create(
                amount=amount,
                phone_number=phone_number,
                user=user,
                ref=ref,
            )
            context = {
                'payment': payment,
                'amount': amount,
                'phone_number': phone_number,
                'user': user,
                'ref': ref,
                'paystack_public_key': settings.PAYSTACK_SECRET_KEY,
              
            }
            # Redirect to the make_payment.html page with context
            return render(request, 'payment/make_payment.html', context)
    # For GET requests, just render the initiate_payment page with an empty form
    return render(request, 'payment/initiate_payment.html')


def verify_payment(request: HttpRequest, ref: str) -> HttpResponse:
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()
    if verified:
        messages.success(request, 'Payment successful')
    else:
        messages.error(request, 'Payment failed')
    return redirect('application-form')
