from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Job


@login_required(login_url="authentication:my-login")
def job_list(request):
    jobs = Job.objects.all().order_by('-posted_date')
    context = {
        'jobs': jobs,
    }
    return render(request, 'jobs/index.html', context)

