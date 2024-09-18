from django.urls import path
from . import views

urlpatterns = [
    path('jobs/', views.job_list, name='job-list'),
    path('jobs/<int:id>', views.job_detail, name='job-detail'),
    # other paths...
]

