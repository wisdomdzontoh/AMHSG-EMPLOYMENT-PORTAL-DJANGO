from django.urls import path
from . import views
from .views import application_form
from .views import get_facilities

urlpatterns = [
    path('job-applications/', views.application_list, name='job-applications'),
    path('application-portal/', views.application_portal, name='application-portal'),
    path('application-portal/form', views.application_form, name='application-form'),
    path('application-portal/form/<int:job_id>/', application_form, name='application_form'),
    path('application/success/', views.application_success, name='application-success'),
    path('get_facilities/<int:region_id>/', get_facilities, name='get_facilities'),
    
    
    #path('application-portal/applicant-details/<int:id>/', views.applicant_details, name='applicant-details'),
    # other paths...
]