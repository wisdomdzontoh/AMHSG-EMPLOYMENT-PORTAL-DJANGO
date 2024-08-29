
from django.conf.urls import handler404
from django.shortcuts import render
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),  # authentication urls for login and signup pages
    path('', include('jobs.urls')),  # jobs
    path('', include('notifications.urls')),  # jobs
    path('', include('application_portal.urls')),
    path('', include('payment.urls')),  #handling of voucher purchase
    
    
    
    path("__reload__/", include("django_browser_reload.urls")),     #browser reload url
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
