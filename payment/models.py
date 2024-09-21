from django.db import models
from django.contrib.auth.models import User
import uuid
import secrets
from .paystack import PayStack
from jobs.models import Job

class Payment(models.Model):
    amount = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  # Allow null values
    job = models.ForeignKey(Job, on_delete=models.CASCADE, default=1)  # Foreign key to Job
    email = models.EmailField(default="ghs@gmail.com")
    ref = models.CharField(max_length=200, unique=True)
    verified = models.BooleanField(default=False)
    payment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-payment_date',)
        
    def __str__(self) -> str:  # Fixed the method name
        return f"{self.user} - Payment of: {self.amount} for {self.job} ({self.verified}) Date:{self.payment_date}"

    def save(self, *args, **kwargs) -> None:
        if not self.ref:
            while True:
                ref = secrets.token_urlsafe(50)
                if not Payment.objects.filter(ref=ref).exists():
                    self.ref = ref
                    break
        super().save(*args, **kwargs)
        
    def amount_value(self) -> int:
        return self.amount * 100  # Converts to cents (kobo) as required by PayStack

    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result['amount'] / 100 == self.amount:  # Ensure that the verified amount matches
                self.verified = True
                self.save()
        return self.verified

class Voucher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    voucher_code = models.CharField(max_length=100, unique=True)
    serial_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    pin = models.CharField(max_length=6, unique=True)
    purchase_date = models.DateTimeField(auto_now_add=True)
    is_redeemed = models.BooleanField(default=False)

    def __str__(self):  # Fixed the method name
        return f"Voucher {self.voucher_code} for {self.user.username}"
