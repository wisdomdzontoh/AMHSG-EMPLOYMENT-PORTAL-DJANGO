from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Payment
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required(login_url="authentication:my-login")
def initiate_payment(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        # Capture the form data from the POST request
        amount = request.POST.get('amount')
        email = request.POST.get('email')
        user = request.user

        # Check if user is authenticated (just an extra precaution)
        if not user.is_authenticated:
            messages.error(request, 'You need to log in to make a payment.')
            return redirect('login')  # Redirect to login page or any other appropriate page

        # Perform any necessary validation here
        if amount and email:
            # Save the payment details to the database
            payment = Payment.objects.create(
                amount=amount,
                email=email,
                user=user  # Ensure user is correctly passed here
            )
            context = {
                'payment': payment,
                'amount': amount,
                'email': email,
                'user': user,
                'ref': payment.ref,  # Use the auto-generated ref from the model
                'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
            }
            # Render the make_payment.html page with context
            return render(request, 'payment/make_payment.html', context)
    # For GET requests, just render the initiate_payment page with an empty form
    return render(request, 'payment/initiate_payment.html')

@login_required(login_url="authentication:my-login")
def verify_payment(request: HttpRequest, ref: str) -> HttpResponse:
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()
    if verified:
        messages.success(request, 'Payment successful')
        return redirect('application-form')
    else:
        messages.error(request, 'Payment failed')
    return redirect('initiate-payment')


@login_required(login_url="authentication:my-login")
def user_transactions(request):
    payments = Payment.objects.filter(user=request.user)
    return render(request, 'payment/user_transactions.html', {'payments': payments})

