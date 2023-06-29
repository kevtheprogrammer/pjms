# from django.shortcuts import render, get_object_or_404,  redirect
# from django.urls import reverse
# from decimal import Decimal
# #from django.core.urlresolvers import reverse
# from django.shortcuts import render
# from django.contrib import messages
# from django.http.response import JsonResponse 
# from django.views.generic.base import TemplateView
# import stripe
# from  cart.models import Order
# from django.contrib.auth.models import User
# from .mobileMoney_form import *
# from .models import *

# from products.models import Category
# from acc.models import Profile
# from cart.models import Order

"""@csrf_exempt
def payment_done(request):
    return render(request,'payment/done.html')

@csrf_exempt
def payment_canceled():
    return render(request,'payment/canceled.html')

def payment_process(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order,id=order_id)
    host = request.get_host()
    bill = float(order.get_it())
    print(order.get_quantity())

    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": "%.2f" % bill ,
        "item_name": f'order {order.id}',
        "invoice":str(order.id),
        'currency_code': 'USD',
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('payment:done')),
        "cancel_return": request.build_absolute_uri(reverse('payment:canceled')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {
        "form": form,
        'order':order, 
        'cat': Category.objects.all(),
        'us': Profile.objects.all()[:10]
        }
    return render(request, "payment/process.html", context)


def MobileMoneyView(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order,id=order_id)
    
    if request.method == 'POST':
        form = MobileMoneyPayment(request.POST,request.FILES) 

        if form.is_valid():
            instance = form.save(False)
            instance.order = order
            instance.save()
            messages.warning(request, ('Your payment is awaiting moderation.'))
            context = {
        'cat': Category.objects.all(),
        'us':  Profile.objects.all()[:10],
    }
            return render(request,'payment/done.html', context )
    else:
        form = MobileMoneyPayment(request.POST,request.FILES)
    context = {
        'form' : MobileMoneyPayment(),
        'cat': Category.objects.all(),
        'us':  Profile.objects.all()[:10],
    }
    return render(request,'payment/mobile_money.html', context )

class StripePayment(TemplateView):
    template_name = 'payment/stripe_payment.html'

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

@csrf_exempt
def stripe_checkout_session(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order,id=order_id)
    bill = float(order.get_it())
    
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/payment/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': f'order {order.id}',
                        'quantity': order.get_quantity(),
                        'currency': 'usd',
                        'amount': "%.2f" % bill,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

def PaymentView(request):
    tmp = 'payment/payment-view.html' 
    data = {
        'pay' : MobileMoney.objects.filter(order__client=request.user.user) ,
        'us' : Profile.objects.all()[:10],
        'cat' : Category.objects.all(),
    }
    return render(request,tmp,data)

def OrderView(request):
    tmp = 'payment/order-view.html' 
    data = {
        'orders' : Order.objects.filter(client_id=request.user.user.id ),
        'us' : Profile.objects.all()[:10],
        'cat' : Category.objects.all(),
    }
    return render(request,tmp,data)"""

from typing import Any, Dict
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.views.generic import FormView
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from product.models import Order


class PaypalFormView(FormView):
    template_name = 'payment/paypal_form.html'
    form_class = PayPalPaymentsForm
 

    def get_initial(self):
        order_id = self.request.session.get('order_id')
        order = get_object_or_404(Order,id=order_id)
        host = self.request.get_host()
        bill = float(order.get_subtotal())
        return {
            'business':  settings.PAYPAL_RECEIVER_EMAIL,
            'amount': "%.2f" % bill,
            'currency_code': 'EUR',
            'item_name': f'order {order.id}',
            'invoice': str(order.id),
            'notify_url': self.request.build_absolute_uri(reverse('paypal-ipn')),
            'return_url': self.request.build_absolute_uri(reverse('payment:done')),
            'cancel_return': self.request.build_absolute_uri(reverse('payment:canceled')),
            'lc': 'EN',
            # 'no_shipping': '1',
        }
    

class PaypalReturnView(TemplateView):
    template_name = 'payment/paypal_success.html'

class PaypalCancelView(TemplateView):
    template_name = 'payment/paypal_cancel.html'


@receiver(valid_ipn_received)
def paypal_payment_received(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the `business` field. (The user could tamper with
        # that fields on the payment form before it goes to PayPal)
        if ipn_obj.receiver_email != settings.PAYPAL_RECEIVER_EMAIL:
            # Not a valid payment
            return

        # ALSO: for the same reason, you need to check the amount
        # received, `custom` etc. are all what you expect or what
        # is allowed.
        try:
            my_pk = ipn_obj.invoice
            mytransaction = MyTransaction.objects.get(pk=my_pk)
            assert ipn_obj.mc_gross == mytransaction.amount and ipn_obj.mc_currency == 'EUR'
        except Exception:
            logger.exception('Paypal ipn_obj data not valid!')
        else:
            mytransaction.paid = True
            mytransaction.save()
    else:
        logger.debug('Paypal payment status not completed: %s' % ipn_obj.payment_status)