# forms.py
from django import forms
from .models import User
from django.core.exceptions import ValidationError
from datetime import date, timedelta

class UserSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'dob', 'expiry', 'ammount']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'expiry': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'ammount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter the ammount'}),
        }

    def clean_dob(self):
        dob = self.cleaned_data.get('dob')
        if dob > date.today() - timedelta(days=18*365):
            raise ValidationError("Date of Birth must indicate an age of at least 18 years.")
        return dob

    def clean_expiry(self):
        expiry = self.cleaned_data.get('expiry')
        if expiry < date.today():
            raise ValidationError("Expiry date cannot be before today.")
        return expiry

    def clean_amount(self):
        amount = self.cleaned_data.get('ammount')
        if amount < 0 or amount > 1_000_000_000:
            raise ValidationError("Amount must be between 0 and 1 billion.")
        return amount

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
