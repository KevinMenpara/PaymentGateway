from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse
import csv
from django.core.mail import send_mail
from payment.models import Payment
from decouple import config

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('ammount', 'payment_time_stamp', 'payment_method', 'status')
