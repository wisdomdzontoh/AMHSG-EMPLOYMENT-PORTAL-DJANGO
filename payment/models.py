from django.db import models
from django.contrib.auth.models import User
import uuid
import secrets
from .paystack import PayStack


class Payment(models.Model):
    amount = models.PositiveIntegerField()
    phone_number = models.CharField(max_length=20)
    user = models.CharField(max_length=200)
    ref = models.CharField(max_length=200)
    verified = models.BooleanField(default=False)
    payment_date = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        ordering = ('-payment_date',)
        
    def __str__(self) -> str:
        return f"Payment of: {self.amount}" 
        
    def save(self, *args, **kwargs) -> None:
        while not self.ref:
            ref = secrets.token_urlsafe(50)
            object_with_similar_ref = Payment.objects.filter(ref=ref)
            if not object_with_similar_ref:
                similar_ref = ref
        super().save(*args, **kwargs)
        
    def amount_value(self) -> int:
        return self.amount * 100  # Convert to GHS with two decimal places


    def __str__(self):
        return f"Payment by {self.user} for {self.amount}"
    

def verify_payment(self):
    paystack = PayStack()
    status, result = paystack.verify_payment(self.ref, self.amount)
    if status:
        if result['amount'] / 100 == self.amount:
            self.verified = True
        self.save()
    if self.verified:
        return True
    return False

class Voucher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    voucher_code = models.CharField(max_length=100, unique=True)
    serial_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    pin = models.CharField(max_length=6, unique=True)
    purchase_date = models.DateTimeField(auto_now_add=True)
    is_redeemed = models.BooleanField(default=False)

    def __str__(self):
        return f"Voucher {self.voucher_code} for {self.user.username}"
