from django.urls import path
from application_portal import views
from . import views

urlpatterns = [
    #path('application-portal/purchase-voucher', views.purchase_voucher, name='purchase-voucher'),
    path('application-portal/payment', views.initiate_payment, name='initiate-payment'),
    path('verify-payment/<str:ref>/<int:job_id>/', views.verify_payment, name='verify-payment'),
    path('application_portal/payment/my-transactions', views.user_transactions, name="my-transactions"),
    
    # other paths...
]