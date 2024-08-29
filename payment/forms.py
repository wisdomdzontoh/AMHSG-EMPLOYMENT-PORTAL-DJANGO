from django import forms
from .models import Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ("amount", "phone_number", "user", "payment_status", "transaction_reference")
