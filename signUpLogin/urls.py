from django.contrib import admin
from django.urls import path

from signUpLogin import views

urlpatterns = [
    path('signup/', views.signUp , name="signUp"),
    path('', views.login , name="login"),
    path('verify-code/', views.verify_code, name='verify_code'),
    path('thankyou/', views.thankyou , name="thankYou"),
]
