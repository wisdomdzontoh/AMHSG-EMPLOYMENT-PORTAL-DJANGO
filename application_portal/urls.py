from django.urls import path
from . import views
from .views import application_form


urlpatterns = [
    path('job-applications/', views.application_list, name='job-applications'),
    path('application-portal/', views.application_portal, name='application-portal'),
    path('application-portal/form', views.application_form, name='application-form'),
    path('application-portal/form/<int:job_id>/', application_form, name='application_form'),
    path('application/success/', views.application_success, name='application-success'),
    
    
    
    # other paths...
]