from django.shortcuts import redirect
from django.contrib import messages
from .models import Payment
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
import random
import string
from jobs.models import Job
from application_portal.models import PersonalInformation, Application
from django.utils import timezone
from .models import Payment
import logging
from django.db import IntegrityError





import logging

logger = logging.getLogger(__name__)

def payment_required(view_func):
    def _wrapped_view(request, *args, **kwargs):  # Modify the decorator to handle any args
        job_id = kwargs.get('job_id') or args[0]  # Ensure job_id is correctly unpacked
        job = get_object_or_404(Job, id=job_id)
        user = request.user
        
        has_applied_for_job = Application.objects.filter(user=user, job=job).exists()
        verified_payments = Payment.objects.filter(user=user, verified=True, job_id=job_id)
        
        if has_applied_for_job:
            logger.debug(f"User {user} has already applied for job {job_id}.")
            messages.error(request, "You have already applied for this job.")
            return redirect('job-detail', id=job.id)
        
        if verified_payments.exists():
            logger.debug(f"User {user} has verified payment for job {job_id}.")
            return view_func(request, *args, **kwargs)  # Pass args and kwargs correctly
        
        logger.debug(f"User {user} does not have a verified payment for job {job_id}.")
        messages.error(request, "You must complete a payment to apply for this job.")
        return redirect('initiate-payment')
        
    return _wrapped_view









