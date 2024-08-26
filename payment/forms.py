from django import forms
from .models import Payment
from django.core.exceptions import ValidationError
from datetime import date, timedelta

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['name', 'dob', 'ammount', 'payment_method']
        
