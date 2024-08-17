import base64
import logging
import random
import string
from django.utils.dateparse import parse_datetime
from decouple import config
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.core.mail import send_mail
from django.shortcuts import render, redirect ,get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponseNotFound, HttpResponseRedirect, JsonResponse,HttpResponse
from datetime import datetime, timedelta
from .forms import UserSignupForm, UserLoginForm
from .models import User,UserPDF
from django.contrib.auth import login as auth_login
from django.template.loader import render_to_string
from io import BytesIO
import logging
from django.db import models
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from django.conf import settings
import base64
from .cipher import CustomCipher
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


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
            email = form.cleaned_data['email']
            raw_password = form.cleaned_data['password']
            dob = form.cleaned_data['dob']
            expiry = form.cleaned_data['expiry']
            name = form.cleaned_data['name']
            ammount = form.cleaned_data['ammount']

            try:
                # Temporarily store signup data in session
                user = User()  # Create an instance of User
                encrypt_password = user.encrypt(raw_password)
                request.session['signup_data'] = {
                    'email': email,
                    'password': encrypt_password,
                    'dob' : dob.isoformat(),  # Convert date to string
                    'expiry' : expiry.isoformat(),  # Convert date to string
                    'name' : name,
                    'ammount' : ammount
                }

                # Generate and store security code in session
                security_code = generate_security_code()
                encrypted_code = user.encrypt(security_code)
                request.session['security_code'] = encrypted_code
                request.session['security_code_expires_at'] = (timezone.now() + timedelta(minutes=5)).isoformat()

                # Send security code via email
                send_security_code_email(email, security_code)

                return JsonResponse({'success': True, 'redirect_url': reverse('verify_code')})
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
            # print(email)
            raw_password = form.cleaned_data['password']
            # print(raw_password)
            try:
                user = User.objects.get(email=email)
                password = user.password
                # print(password)
                # print(user.encrypt(raw_password))
                # print(user.decrypt(password))
                # print(user.check_password(raw_password))
                if user.encrypt(raw_password) == user.decrypt(password):
                    # Temporarily store login data in session
                    request.session['login_data'] = {'user_id': user.id}

                    # Generate and store security code in session
                    security_code = generate_security_code()
                    encrypted_code = user.encrypt(security_code)
                    request.session['security_code'] = encrypted_code
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
        encrypted_code = request.session.get('security_code')
        expires_at_str = request.session.get('security_code_expires_at')

        if encrypted_code and expires_at_str:
            expires_at = parse_datetime(expires_at_str)

            if expires_at is None:
                return JsonResponse({'error': 'Invalid expiration time format.'}, status=400)

            if timezone.now() > expires_at:
                return JsonResponse({'error': 'Security code expired.'}, status=400)

            user_cipher = CustomCipher()
            decrypted_code = user_cipher.decrypt(encrypted_code)

            if code == decrypted_code:
                signup_data = request.session.get('signup_data')
                login_data = request.session.get('login_data')

                if login_data:
                    user_id = login_data.get('user_id')
                    if user_id:
                        try:
                            print(user_id)
                            user = User.objects.get(id=user_id)
                            auth_login(request, user)
                            request.session.pop('login_data', None)
                            return JsonResponse({'success': True, 'thank_you_url': reverse('thankYou')})
                        except User.DoesNotExist:
                            return JsonResponse({'error': 'User not found.'}, status=404)
                    else:
                        return JsonResponse({'error': 'User ID not found in session.'}, status=404)

                elif signup_data:
                    try:
                        dob = parse_datetime(signup_data['dob']).date()
                        expiry = parse_datetime(signup_data['expiry']).date()
                        print(dob)
                        user = User(
                            name=signup_data['name'],
                            email=signup_data['email'],
                            dob=dob,
                            expiry=expiry,
                            ammount=signup_data['ammount']
                        )
                        user.set_password(signup_data['password'])
                        user.save()

                        # Generate PDF and get the file path
                        pdf_file_path = generate_user_pdf(user.id)
                        pdf = UserPDF(
                            user=user,
                            pdf_file_path=pdf_file_path
                        )
                        pdf.save()
                        

                        # Redirect to the PDF download URL with a flag for redirection to thank you page
                        response = JsonResponse({'success': True, 'pdf_url': reverse('download_pdf', kwargs={'file_path': pdf_file_path}), 'thank_you_url': reverse('thankYou')})
                        return response

                    except Exception as e:
                        logger.error(f"Signup data error: {str(e)}")
                        return JsonResponse({'error': 'Failed to create user. Please try again later.'}, status=500)


            return JsonResponse({'error': 'Invalid security code.'}, status=400)

        return JsonResponse({'error': 'Security code not found.'}, status=400)

    return render(request, 'signUpLogin/verify_code.html')


def thankyou(request):
    return render(request, 'signUpLogin/thankyou.html')


def generate_user_pdf(user_id):
    user = User.objects.get(id=user_id)

    # Create a buffer for the PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    p.drawString(100, height - 100, f"Name: {user.name}")
    p.drawString(100, height - 120, f"Email: {user.email}")
    p.drawString(100, height - 140, f"Date of Birth: {user.dob}")
    p.drawString(100, height - 160, f"Expiry Date: {user.expiry}")
    p.drawString(100, height - 180, f"Amount: ${user.ammount}")
    p.drawString(100, height - 200, f"Created At: {user.created_at}")

    p.showPage()
    p.save()

    buffer.seek(0)
    pdf_file_path = f"user_{user_id}_info.pdf"

    # Save PDF to the default storage (e.g., local filesystem or cloud storage)
    file_path = default_storage.save(pdf_file_path, ContentFile(buffer.getvalue()))
    return file_path


def download_pdf(request, file_path):
    if default_storage.exists(file_path):
        pdf_file = default_storage.open(file_path, 'rb')
        response = HttpResponse(pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{file_path}"'
        pdf_file.close()
        return response
    else:
        return HttpResponseNotFound('File not found')



# def serve_pdf(request, user_id):
#     user_pdf = get_object_or_404(UserPDF, user_id=user_id)
#     response = HttpResponse(user_pdf.pdf_file, content_type='application/pdf')
#     response['Content-Disposition'] = f'attachment; filename="user_{user_id}_info.pdf"'
#     return response

