from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login as auth_login
from django.http import HttpResponseNotFound, JsonResponse

from signUpLogin.models import User
from .forms import UserSignupForm, UserLoginForm
import logging

# Set up logging
logger = logging.getLogger(__name__)

def signUp(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                auth_login(request, user)
                return JsonResponse({'success': True})
            except Exception as e:
                logger.error(f"Signup error: {str(e)}")
                return JsonResponse({'error': str(e)}, status=500)
        else:
            errors = form.errors.as_json()
            return JsonResponse({'error': errors}, status=400)
    else:
        form = UserSignupForm()
        # google_login_url = reverse('google_login')
        google_login_url = '''https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?client_id=682080890766-vsiogr9obv1ov0uvigm9efmpllmq4ihc.apps.googleusercontent.com&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Faccounts%2Fgoogle%2Flogin%2Fcallback%2F&scope=profile&response_type=code&state=queMZ4KPBVLXNkaJ&service=lso&o2v=2&ddm=0&flowName=GeneralOAuthFlow'''
    return render(request, 'signUpLogin/signUp.html', {'form': form, 'google_login_url': google_login_url})

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            raw_password = form.cleaned_data['password']
            try:
                user = User.objects.get(email=email)
                if user.check_password(raw_password):
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({'error': 'Invalid email or password.'}, status=401)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User does not exist.'}, status=404)
        else:
            errors = form.errors.as_json()
            return JsonResponse({'error': errors}, status=400)
    else:
        form = UserLoginForm()
    return render(request, 'signUpLogin/login.html', {'form': form})

def thankyou(request):
    try:
        # thankyou_template = loader.get_template("signUpLogin/thankYou.html")
        context = {}
        return render(request,"signUpLogin/thankYou.html",context)
        # return HttpResponse(thankyou_template.render(context,request))
    except:
        return HttpResponseNotFound("Error in thankYou.html")