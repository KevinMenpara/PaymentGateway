from django import forms
from django.http import HttpResponse,HttpResponseNotFound, JsonResponse
from django.shortcuts import render,redirect
from django.urls import reverse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login as auth_login
from signUpLogin.forms import UserSignupForm
# Create your views here.

def signUp(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return JsonResponse({'success': True})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        else:
            errors = form.errors.as_json()
            return JsonResponse({'error': errors}, status=400)
    else:
        form = UserSignupForm()
    return render(request, 'signUpLogin/signUp.html', {'form': form})  

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

@csrf_exempt
def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                auth_login(request, user)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'Invalid email or password'}, status=400)
        else:
            errors = form.errors.as_json()
            return JsonResponse({'error': errors}, status=400)
    else:
        form = LoginForm()
        return render(request, 'signUpLogin/login.html', {'form': form})
    

def thankyou(request):
    try:
        # thankyou_template = loader.get_template("signUpLogin/thankYou.html")
        context = {}
        return render(request,"signUpLogin/thankYou.html",context)
        # return HttpResponse(thankyou_template.render(context,request))
    except:
        return HttpResponseNotFound("Error in thankYou.html")