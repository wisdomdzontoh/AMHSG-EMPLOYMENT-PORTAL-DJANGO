from django.db import models
from django.contrib.auth.models import User
import uuid

class Voucher(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    voucher_code = models.CharField(max_length=100, unique=True)
    serial_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    pin = models.CharField(max_length=6, unique=True)
    purchase_date = models.DateTimeField(auto_now_add=True)
    is_redeemed = models.BooleanField(default=False)

    def __str__(self):
        return f"Voucher {self.voucher_code} for {self.user.username}"
