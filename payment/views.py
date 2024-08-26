from django.shortcuts import render, get_object_or_404
from .models import Payment

def payment_detail(request, transaction_id):
    # Fetch the payment object based on the transaction_id from the URL
    payment = get_object_or_404(Payment, transaction_id=transaction_id)
    
    # You can perform any additional logic here or pass the payment to a template
    context = {'payment': payment}
    return render(request, 'payment/payment_form.html', context)
