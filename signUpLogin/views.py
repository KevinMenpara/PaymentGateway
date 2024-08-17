import logging
import random
import string
from django.utils.dateparse import parse_datetime
from decouple import config
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.http import JsonResponse, HttpResponseNotFound
from datetime import datetime, timedelta
from .forms import UserSignupForm, UserLoginForm
from .models import User
from django.contrib.auth import login as auth_login

# Set up logging
logger = logging.getLogger(__name__)

def generate_security_code():
    """Generate a random 6-digit security code."""
    return ''.join(random.choices(string.digits, k=6))

def send_security_code_email(email, security_code):
    """Send the security code via email."""
    try:
        send_mail(
            'Your Security Code',
            f'Your security code is {security_code}. It expires in 5 minutes.',
            config('EMAIL_HOST_USER'),  # Replace with your email address
            [email],
            fail_silently=False,
        )
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")
        raise

def signUp(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            try:
                # Temporarily store signup data in session
                request.session['signup_data'] = {
                    'email': form.cleaned_data['email'],
                    'password': form.cleaned_data['password'],
                }

                # Generate and store security code in session
                security_code = generate_security_code()
                request.session['security_code'] = security_code
                request.session['security_code_expires_at'] = (timezone.now() + timedelta(minutes=5)).isoformat()

                # Send security code via email
                send_security_code_email(form.cleaned_data['email'], security_code)

                return redirect('verify_code')  # Redirect to verification page
            except Exception as e:
                logger.error(f"Signup error: {str(e)}")
                return JsonResponse({'error': 'Failed to process signup. Please try again later.'}, status=500)
        else:
            errors = form.errors.as_json()
            return JsonResponse({'error': errors}, status=400)
    else:
        form = UserSignupForm()
    return render(request, 'signUpLogin/signUp.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            raw_password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                if user.check_password(raw_password):
                    # Temporarily store login data in session
                    request.session['login_data'] = {'user_id': user.id}

                    # Generate and store security code in session
                    security_code = generate_security_code()
                    request.session['security_code'] = security_code
                    request.session['security_code_expires_at'] = (timezone.now() + timedelta(minutes=5)).isoformat()

                    # Send security code via email
                    send_security_code_email(email, security_code)

                    return JsonResponse({'success': True, 'redirect_url': reverse('verify_code')})
                else:
                    return JsonResponse({'error': 'Invalid email or password.'}, status=401)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User does not exist.'}, status=404)
            except Exception as e:
                logger.error(f"Login error: {str(e)}")
                return JsonResponse({'error': 'Failed to process login. Please try again later.'}, status=500)
        else:
            errors = form.errors.as_json()
            return JsonResponse({'error': errors}, status=400)
    else:
        form = UserLoginForm()
    return render(request, 'signUpLogin/login.html', {'form': form})

def verify_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        stored_code = request.session.get('security_code')
        expires_at_str = request.session.get('security_code_expires_at')

        if stored_code and expires_at_str:
            # Parse the expiration time
            expires_at = parse_datetime(expires_at_str)

            if expires_at is None:
                return JsonResponse({'error': 'Invalid expiration time format.'}, status=400)

            # Check if the expiration time is valid
            if timezone.now() > expires_at:
                return JsonResponse({'error': 'Security code expired.'}, status=400)

            if code == stored_code:
                # Security code is valid, log the user in and redirect
                user_id = request.session.get('login_data', {}).get('user_id')
                if user_id:
                    try:
                        user = User.objects.get(id=user_id)
                        auth_login(request, user)
                        return JsonResponse({'success': True, 'redirect_url': reverse('thankYou')})
                    except User.DoesNotExist:
                        return JsonResponse({'error': 'User not found.'}, status=404)
                return JsonResponse({'error': 'User ID not found in session.'}, status=404)

            return JsonResponse({'error': 'Invalid security code.'}, status=400)

        return JsonResponse({'error': 'Security code not found.'}, status=400)

    # For GET request, render the verification form
    return render(request, 'signUpLogin/verify_code.html')

def thankyou(request):
    return render(request, 'signUpLogin/thankyou.html')

