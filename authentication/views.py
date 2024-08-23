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




# Homepage view
def homepage(request):
    return render(request, 'authentication/index.html')

# User registration view
def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken. Please choose a different one.")
            elif User.objects.filter(email=email).exists():
                messages.error(request, "Email already registered. Please use a different one.")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
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
@login_required(login_url="my-login")
def dashboard(request):
    jobs = Job.objects.all().order_by('-posted_date')[:5]
    notifications = Notification.objects.all().order_by('-date')[:5]
    context = {
        'jobs': jobs,
        'notifications': notifications,
    }
    return render(request, 'authentication/dashboard.html', context)
