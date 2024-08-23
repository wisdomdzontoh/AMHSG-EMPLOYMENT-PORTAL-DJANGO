from django.shortcuts import render
from .models import Notification

def notification_list(request):
    notifications = Notification.objects.all().order_by('-date')
    context = {
        'notifications': notifications,
    }
    return render(request, 'notifications/index.html', context)

