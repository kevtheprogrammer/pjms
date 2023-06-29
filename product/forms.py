from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
 

from .models import *
from stock.models import *

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'thumb','name','description','price','discount','category','slug'
        ]
  
class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = [
            'quantity',
            ]

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'status',
            ]
  
class StockForm(forms.ModelForm):
    class Meta:
        model = StockModel
        fields = [
            'prod','quantity','slug'
            ]


class StockEditForm(forms.ModelForm):
    class Meta:
        model = StockModel
        fields = [
            'quantity',
        ]



class CheckOutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
			# 'orderitems',
			'email',
			'address',
			'city',
			'state',
			'zip_code',
			# 'shipping_fee',
			)
        # widgets = {
        #     'orderitems': forms.CheckboxSelectMultiple,
        # }