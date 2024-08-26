from django.contrib import admin
from django.urls import path

from payment import views

urlpatterns = [
    path('<uuid:transaction_id>/', views.payment_detail, name='payment_detail'),
]
