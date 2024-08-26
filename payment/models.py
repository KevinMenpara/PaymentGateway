import uuid
from django.db import models
from signUpLogin.models import User,UserPDF

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    ammount = models.PositiveIntegerField(default=0)
    payment_time_stamp = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    status = models.CharField(max_length=20, default='Pending')

    def __str__(self):
        return f"{self.user.name} - {self.transaction_id}"
