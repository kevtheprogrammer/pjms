from django.contrib import admin
from django.urls import path

from django.contrib.auth.decorators import login_required

from .views import *

app_name = "payment" 

# urlpatterns = [
#     path('process/', login_required(payment_process), name="process"),
#     path('success/', login_required(payment_done),name="done"),
#     path('cancelled/', login_required(payment_canceled),name="canceled"),
#     path('mobile-money/', login_required(MobileMoneyView),name="mobileMoney"),
#     path('config/', login_required(stripe_config),name="stripe"),
#     path('checkout-session/',login_required(stripe_checkout_session), name = "stipe-checkout"),
#     path('my-payments/',login_required(PaymentView),name="view"),
#     path('my-orders/',login_required(OrderView),name="order"),    
# ]   


from . import views
urlpatterns = [
    path('process-payment/', PaypalFormView.as_view(), name='process-payment'),
    path('paypal-return/', PaypalReturnView.as_view(), name='done'),
    path('paypal-cancel/', PaypalCancelView.as_view(), name='canceled'),
]