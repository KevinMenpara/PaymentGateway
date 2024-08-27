import uuid
from django.db import models
from signUpLogin.models import User

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    ammount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_time_stamp = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
    # Optional: Status with choices
    PENDING = 'Pending'
    COMPLETED = 'Completed'
    FAILED = 'Failed'
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETED, 'Completed'),
        (FAILED, 'Failed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    
    def __str__(self):
        return f"{self.user.name} - {self.transaction_id}"

    class Meta:
        ordering = ['-payment_time_stamp']  # Order by newest first
