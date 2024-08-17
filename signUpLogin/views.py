import logging
from .models import User
from django import forms
from django.urls import reverse
from django.template import loader
from django.shortcuts import render,redirect
from .forms import UserSignupForm, UserLoginForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login
from django.http import HttpResponse,HttpResponseNotFound, JsonResponse
# Create your views here.


# Set up logging
logger = logging.getLogger(__name__)

def signUp(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return JsonResponse({'success': True})
            except Exception as e:
                logger.error(f"Signup error: {str(e)}")
                return JsonResponse({'error': str(e)}, status=500)
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