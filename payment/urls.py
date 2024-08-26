from django.urls import path
from application_portal import views

urlpatterns = [
    path('application-portal/purchase-voucher', views.purchase_voucher, name='purchase-voucher'),
    # other paths...
]