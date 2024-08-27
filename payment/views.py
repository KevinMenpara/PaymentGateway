from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Payment
from signUpLogin.models import User
from .forms import PaymentForm

def payment_redirect(request, transaction_id, ammount):
    """Redirect users based on authentication status."""
    if request.session.get('check_login'):
        # Fetch user email from GET parameters
        useremail = request.GET.get('useremail')
        if not useremail:
            return redirect(reverse('payment:payment_error'))

        user = get_object_or_404(User, email=useremail)

        if request.method == 'POST':
            form = PaymentForm(request.POST, ammount=ammount, email=useremail)
            if form.is_valid():
                dob = form.cleaned_data['dob']
                payment_method = form.cleaned_data['payment_method']

                # Validate the payment conditions
                if ammount <= user.ammount and dob == user.dob:
                    # Create a new payment record
                    payment = Payment(
                        transaction_id=transaction_id,
                        user=user,
                        ammount=ammount,
                        payment_method=payment_method,
                        status = 'Success'
                    )
                    payment.save()

                    # Deduct the amount from the user's balance
                    user.ammount -= ammount
                    user.save()

                    # Redirect to the thank you page
                    return redirect(reverse('thankYou'))
                else:
                    return redirect(reverse('paymentError'))
            else:
                return redirect(reverse('paymentError'))
        else:
            form = PaymentForm(ammount=ammount, email=useremail)

        context = {
            'transaction_id': transaction_id,
            'ammount': ammount,
            'form': form
        }
        return render(request, 'payment/payment.html', context)
    else:
        return redirect(reverse('login'))

def payment_error(request):
    return render(request, 'payment/paymentError.html')