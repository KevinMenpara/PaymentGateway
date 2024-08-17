from django.contrib import admin
from django.urls import path

from signUpLogin import views

urlpatterns = [
    path('signup/', views.signUp , name="signUp"),
    path('', views.login , name="login"),
    path('thankyou/', views.thankyou , name="thankYou"),
]
