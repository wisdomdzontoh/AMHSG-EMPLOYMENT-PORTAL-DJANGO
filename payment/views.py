from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Payment
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from jobs.models import Job




@login_required(login_url="authentication:my-login")
def initiate_payment(request: HttpRequest) -> HttpResponse:
    jobs = Job.objects.all()

    if request.method == "POST":
        amount = request.POST.get('amount')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        job_id = request.POST.get('job_id')
        user = request.user

        if job_id:
            job = get_object_or_404(Job, id=job_id)
        else:
            messages.error(request, 'Job not found.')
            return redirect('job-list')

        if not user.is_authenticated:
            messages.error(request, 'You need to log in to make a payment.')
            return redirect('my-login')

        if amount and email and phone:
            payment = Payment.objects.create(
                amount=amount,
                email=email,
                phone=phone,
                user=user,
                job_id=job_id
            )
            context = {
                'payment': payment,
                'amount': amount,
                'email': email,
                'phone': phone,
                'user': user,
                'jobs': jobs,  # Make sure jobs is included here
                'job': job,
                'ref': payment.ref,
                'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
            }
            return render(request, 'payment/make_payment.html', context)

    return render(request, 'payment/initiate_payment.html', {'jobs': jobs})  # Include jobs in the context




@login_required(login_url="authentication:my-login")
def verify_payment(request: HttpRequest, ref: str, job_id: int) -> HttpResponse:
    payment = get_object_or_404(Payment, ref=ref)
    verified = payment.verify_payment()

    if verified:
        messages.success(request, 'Payment successful')
        return redirect('application_form', job_id=job_id)
    else:
        messages.error(request, 'Payment failed')

    return redirect('initiate-payment')




@login_required(login_url="authentication:my-login")
def user_transactions(request):
    payments = Payment.objects.filter(user=request.user)
    return render(request, 'payment/user_transactions.html', {'payments': payments})

