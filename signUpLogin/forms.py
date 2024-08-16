# forms.py
from django import forms
from .models import User

class UserSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'dob', 'expiry', 'ammount']  # Fixed typo
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'expiry': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'ammount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter the ammount'}),
        }

