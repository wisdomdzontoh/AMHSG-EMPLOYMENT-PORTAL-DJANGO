from django.shortcuts import render
from .models import Application
from django.contrib.auth.decorators import login_required

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

