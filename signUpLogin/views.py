from django.http import HttpResponse,HttpResponseNotFound
from django.shortcuts import render,redirect
from django.urls import reverse
from django.template import loader

# Create your views here.

def signUp(request):
    try:
        # signup_template = loader.get_template("signUpLogin/signUp.html")
        context = {"login_url":reverse('login')}
        # return HttpResponse(signup_template.render(context,request))
        return render(request,"signUpLogin/signUp.html",context)
    except:
        return HttpResponseNotFound("Error in signUp.html")

def login(request):
    try:
        # login_template = loader.get_template("signUpLogin/login.html")
        context = {"signUp_url":reverse('signUp')}
        return render(request,"signUpLogin/login.html",context)
        # return HttpResponse(login_template.render(context,request))
    except:
        return HttpResponseNotFound("Error in login.html")

def thankyou(request):
    try:
        # thankyou_template = loader.get_template("signUpLogin/thankYou.html")
        context = {"home_url":reverse('login')}
        return render(request,"signUpLogin/thankYou.html",context)
        # return HttpResponse(thankyou_template.render(context,request))
    except:
        return HttpResponseNotFound("Error in thankYou.html")