# forms.py
from django import forms

class PaymentForm(forms.Form):
    dob = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))
    payment_method = forms.ChoiceField(choices=[
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer')
    ])
    ammount = forms.DecimalField(max_digits=10, decimal_places=2, disabled=True)
    email = forms.EmailField(disabled=True)

    def __init__(self, *args, **kwargs):
        ammount = kwargs.pop('ammount', None)
        email = kwargs.pop('email', None)
        super().__init__(*args, **kwargs)
        if ammount is not None:
            self.fields['ammount'].initial = ammount
        if email is not None:
            self.fields['email'].initial = email
