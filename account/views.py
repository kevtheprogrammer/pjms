from django.shortcuts import render,get_object_or_404,redirect

from django.contrib import messages
import json

from django.views.generic import ListView , DetailView ,View,TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import User
from stock.models import StockModel
from product.forms import ProductForm,OrderForm
from product.forms import StockForm,StockEditForm
from product.models import Category, Product,Tag, Order



class AdminIndexView(TemplateView):
    template_name = "mngmnt/index.html"
    form_class = ProductForm 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.all() 
        context["form"] = ProductForm() 
        context["product_list_4"] = Product.objects.all()[:4] 
        context["order_5"] = Order.objects.all()[:7] 
        context["stock_5"] = StockModel.objects.all()[:7] 
        context["tags"] = Tag.objects.all() 
        return context 
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST,request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user 
            instance.save()
            return redirect('account:products')
        return redirect('account:dashboard')

class CustomerListView(ListView):
    model = User
    template_name = "mngmnt/customers.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.all() 
        context["form"] = ProductForm() 
        context["object_list_3"] = Product.objects.all()[:3] 
        context["tags"] = Tag.objects.all() 
        return context 

class ProductListView(ListView):
    model = Product
    template_name = "mngmnt/products.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.all() 
        context["form"] = ProductForm() 
        context["product_form"] = ProductForm() 
        context["object_list_3"] = Product.objects.all()[:3] 
        context["tags"] = Tag.objects.all() 
        return context 

class ProductDetailView(DetailView):
    model = Product
    template_name = "mngmnt/prod_details.html"
    form_class = ProductForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.all() 
        context["form"] =  self.form_class()
        context["forms"] = ProductForm(instance=self.get_object()) 
        context["object_list_3"] = Product.objects.all()[:3] 
        context["tags"] = Tag.objects.all() 
        return context 
    
    def post(self,request, *args, **kwargs):
        obj = self.get_object()
        forms = self.form_class(request.POST,request.FILES,instance=self.get_object())
        if forms.is_valid():
            forms.save()
        return redirect(obj.get_absolute_url_admin())

class OrderListView(ListView):
    model = Order
    template_name = "mngmnt/orders.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.all() 
        context["form"] = ProductForm() 
        context["object_list_3"] = Product.objects.all()[:3] 
        context["tags"] = Tag.objects.all() 
        return context 

class OrderDetailView(DeleteView):
    model = Order
    template_name = 'mngmnt/order_details.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.all() 
        context["order_forms"] = OrderForm(instance=self.get_object()) 
        context["object_list_3"] = Product.objects.all()[:3] 
        context["tags"] = Tag.objects.all() 
        return context 
    
    def post(self, *args,**kwargs):
        order_forms = OrderForm(self.request.POST,instance=self.get_object(), )  
        if order_forms.is_valid():
            order_forms.save()
        return redirect(self.get_object().view_order_url())

class WatchListView(ListView):
    model = Product
    template_name = "mngmnt/watch.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.all() 
        context["form"] = ProductForm() 
        context["object_list_3"] = Product.objects.all()[:3] 
        context["tags"] = Tag.objects.all() 
        return context 

class StockListView(ListView):
    model = StockModel
    template_name = "mngmnt/stock.html"
    form_class = StockForm
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.all() 
        context["form"] = ProductForm() 
        context["add_stock_form"] = self.form_class() 
        context["object_list_3"] = Product.objects.all()[:3] 
        context["tags"] = Tag.objects.all() 
        return context 

    def post(self,request, *args, **kwargs):
        add_stock_form = self.form_class(request.POST)
        if add_stock_form.is_valid():
            add_stock_form.save()
        return redirect('account:stock')


class StockDetailView(DeleteView):
    model = StockModel
    form_class = StockEditForm
    template_name = 'mngmnt/stock_details.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.all() 
        context["add_stock_form"] = self.form_class(instance=self.get_object()) 
        context["object_list_3"] = Product.objects.all()[:3] 
        context["tags"] = Tag.objects.all() 
        return context 
    
    def post(self,request, *args,**kwargs):
        obj = self.get_object()
        add_stock_form = self.form_class(request.POST,instance=obj)   
        if add_stock_form.is_valid():
            add_stock_form.save()
        return redirect(obj.get_absolute_url())

