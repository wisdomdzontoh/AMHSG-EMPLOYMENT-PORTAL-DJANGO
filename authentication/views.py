from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CreateUserForm, LoginForm
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout  # Authentication models/views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from jobs.models import Job
from notifications.models import Notification
from application_portal.models import Application




# Homepage view
def homepage(request):
    return render(request, 'authentication/index.html')


def how_to_apply(request):
    return render(request, 'authentication/how-to-apply.html')

def contact_us(request):
    return render(request, 'authentication/contact-us.html')


def about_us(request):
    return render(request, 'authentication/about-us.html')



# User registration view
def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered")
            else:
                user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
                user.save()
                messages.success(request, f"Account created for {username}. You can now log in.")
                
                return redirect("my-login")
        else:
            messages.error(request, "Passwords do not match. Please try again.")
    
    return render(request, 'authentication/register.html')



# User login view
def my_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                auth.login(request, user)
                messages.success(request, "Login successful.")
                return redirect("dashboard")
        else:
            messages.error(request, "Invalid credentials, please try again.")
    
    context = {'loginform': form}
    return render(request, 'authentication/my-login.html', context=context)




@login_required(login_url="authentication:my-login")
# User logout view
def user_logout(request):
    auth.logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("my-login")  # Redirect to homepage after logout

# Dashboard view (requires login)
@login_required(login_url="authentication:my-login")
def dashboard(request):
    # Fetch the latest jobs and notifications
    jobs = Job.objects.all().order_by('-posted_date')[:4]
    notifications = Notification.objects.all().order_by('-date')[:5]

    # Calculate statistics
    total_jobs = Job.objects.count()  # Total number of jobs
    total_applications = Application.objects.filter(user=request.user)  # Total number of applications
    accepted_applications = Application.objects.filter(user=request.user, status='accepted').count()  # Count of accepted applications
    pending_applications = Application.objects.filter(user=request.user, status='pending').count()  # Count of pending applications
    under_review_applications = Application.objects.filter(user=request.user, status='under review').count()  # Count of under review applications

    # Context data to pass to the template
    context = {
        'jobs': jobs,
        'notifications': notifications,
        'total_jobs': total_jobs,
        'total_applications': total_applications.count(),
        'accepted_applications': accepted_applications,
        'pending_applications': pending_applications,
        'under_review_applications': under_review_applications,
    }

    return render(request, 'authentication/dashboard.html', context)
