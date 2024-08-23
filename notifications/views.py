from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required(login_url="my-login")
def notification_list(request):
    notifications = Notification.objects.all().order_by('-date')
    context = {
        'notifications': notifications,
    }
    return render(request, 'notifications/index.html', context)

