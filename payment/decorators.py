from django.shortcuts import redirect
from django.contrib import messages
from .models import Payment

def payment_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user has any verified payments
        if request.user.is_authenticated:
            # Filter payments that are verified and belong to the current user
            has_verified_payment = Payment.objects.filter(user=request.user, verified=True).exists()
            
            if has_verified_payment:
                # If the user has a verified payment, allow access to the view
                return view_func(request, *args, **kwargs)
            else:
                # If no verified payment, redirect to the payment verification page
                messages.error(request, "You must complete a payment to access this page.")
                return redirect('initiate-payment')  # Redirect to the payment initiation page or a specific page
        else:
            # If the user is not authenticated, redirect to login
            return redirect('login')
    return _wrapped_view
