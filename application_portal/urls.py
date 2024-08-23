from django.urls import path
from . import views

urlpatterns = [
    path('job-applications/', views.application_list, name='job-applications'),
    # other paths...
]