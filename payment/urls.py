from django.urls import path
from . import views

urlpatterns = [
    path('<uuid:transaction_id>/<int:ammount>/', views.payment_redirect, name='payment_redirect'),
    path('payment_error', views.payment_error , name='paymentError'),
]
