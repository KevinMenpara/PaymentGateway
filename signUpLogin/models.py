from uuid import uuid4
from django.db import models

# Create your models here.
class User(models.Model):
    checkid = models.UUIDField(default=uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.TextField()  # Assuming AES256 encrypted password
    dob = models.DateField()
    expiry = models.DateField() 
    ammount = models.IntegerField()  # Changed to IntegerField for numerical values
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
