from django.urls import path
from . import views

urlpatterns = [
    path('job-applications/', views.application_list, name='job-applications'),
    path('application-portal/', views.application_portal, name='application-portal'),
    path('application-portal/form', views.application_form, name='application-form'),
    path('application-portal/form/', views.application_form, name='application_form'),
    
    
    # other paths...
]