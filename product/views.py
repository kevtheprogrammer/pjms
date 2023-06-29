from django.shortcuts import render,get_object_or_404,redirect

from django.contrib import messages
import json

from django.views.generic import ListView , DetailView ,View,TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .forms import CartForm, CheckOutForm

from stock.models import StockModel
from .models import Cart, Category, Order, Product, Tag 



class HomeListView(ListView):
    model = Product
    template_name = "index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.all() 
        context["object_list_3"] = Product.objects.all()[:3] 
        context["tags"] = Tag.objects.all() 
        return context 

class ShopListView(ListView):
    model = Product
    paginate_by = 9
    query_set = 'object_list'
    template_name = "product/shop.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pro =  []
        for p in Product.objects.all():
            if p.discount > 0:
                pro.append(p)
        context["category"] = Category.objects.all() 
        context["object_list_5"] = Product.objects.all()[:5] 
        context["tags"] = Tag.objects.all() 
        context["product_discount"] = pro
        return context 

class ProductDetailView(DetailView):
    model = Product
    template_name = "product/detail.html"
    form_class = CartForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        stocks = ([x.quantity for x in StockModel.objects.filter(prod=self.get_object()) ])
        prod = get_object_or_404(Product,pk=self.get_object().pk)
        is_favourite = False
        if prod.favourite.filter(id=self.request.user.id).exists():
            is_favourite = True
        context["is_favourite"] =  is_favourite
        context["category"] = Category.objects.all() 
        context["object_stock"] =  sum(stocks)
        context["object_list_3"] = Product.objects.all()[:3] 
        context["form"] = self.form_class() 
        context["tags"] = Tag.objects.all() 
        context["object_tags"] = Product.objects.filter(tags__in=self.get_object().tags.all()).distinct()  
        return context 
    
    def post(self, *args, **kwargs ):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            instance = form.save(False)
            instance.buyer = self.request.user 
            instance.item = self.get_object()
            instance.save()
        return redirect('product:cart')
        
class AboutUsView(TemplateView):
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = Category.objects.all() 
        context["object_list_3"] = Product.objects.all()[:3] 
        context["tags"] = Tag.objects.all() 
        return context 

class FavouriteView(TemplateView):
    template_name = "product/favourite.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_prod = Product.objects.filter(favourite=self.request.user)
        context["favourite"] = my_prod
        context["category"] = Category.objects.all() 
        context["tags"] = Tag.objects.all() 
        return context 

class FavouriteToggleView(CreateView):
    model = Product
  
    def get( self, request,pk, *args, **kwargs ):
        prod = get_object_or_404(Product, pk=pk)
        if prod.favourite.filter(id=self.request.user.id).exists():
            prod.favourite.remove(request.user)
        else:
            prod.favourite.add(request.user)
        return redirect('product:favourite')            
 
class CartView(TemplateView):
    template_name = "product/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        my_cart = Cart.objects.filter(buyer=self.request.user)
        total_price_cart =  [x.get_cart_total() for x in my_cart ]
        context["category"] = Category.objects.all() 
        context["tags"] = Tag.objects.all() 
        context["cart"] = my_cart
        context["total_price_cart"] = sum(total_price_cart) 
        return context 

class CartCreateView(CreateView):
    model = Cart
  
    def get( self, request,pk, *args, **kwargs ):
        item = get_object_or_404(Product,pk=pk)
        order_item, created = Cart.objects.get_or_create(
            item=item,
            buyer=request.user
        )
        order_qs = Order.objects.filter(client=request.user, ordered=False)
        if order_qs.exists():
            order = order_qs[0]
			# check if the order item is in the order
            if order.orderitems.filter(item__pk=item.pk).exists():
                order_item.quantity += 1
                order_item.save()
                messages.info(request, "This item quantity was updated.")
                return redirect("product:cart")
            else:
                order.orderitems.add(order_item)
                messages.info(request, "This item has been added to your cart.")
                return redirect("product:cart")
        else:
            order = Order.objects.create(
                client=request.user.user)
            order.orderitems.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("product:cart")

class CheckOutCreateView(CreateView):
    model = Order
    form_class = CheckOutForm
    template_name = 'product/checkout_form.html'

    # def get_form(self, *args, **kwargs):
    #     form = super().get_form(*args, **kwargs)  # Get the form as usual
    #     user = self.request.user
    #     form.fields['shipping_fee'].queryset = Cart.objects.filter(buyer=user)
    #     return form

    def get_context_data(self, *args, **kwargs):
        user = self.request.user
        subtotal = [x.get_cart_total() for x in Cart.objects.filter(buyer=user)]
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        context['products'] = Product.objects.all()
        context['cart'] = Cart.objects.filter(buyer=user)
        context['subtotal'] = sum(subtotal)
        return context

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        user = self.request.user
        # form.fields['orderitems'].queryset = Cart.objects.filter(buyer=user)
        cart = Cart.objects.filter(buyer=user)
        
        if form.is_valid():
            instance = form.save(commit=False)
            # instance.ordered = True
            instance.client_id = user.id
            
            instance.save()
            form.save_m2m()
            instance.orderitems.set(cart)  
            request.session['order_id'] = instance.pk
            return redirect("payment:process-payment")
        return render(request,self.template_name,{'form':form})#,'forms' : forms})

class CartDeleteView(DeleteView):
    model = Cart

    def get( self, request,pk, *args, **kwargs ):
        item = get_object_or_404(Product,pk=pk)
        cart_qs = Cart.objects.filter(buyer=request.user, item=item)
        if cart_qs.exists():
            cart_qs.delete()
        order_qs = Order.objects.filter(client=request.user,ordered=False)
        if order_qs.exists():
            order = order_qs[0]
            if order.orderitems.filter(item__pk=item.pk).exists():
                order_item = Cart.objects.filter(
                    item=item,
                    buyer=request.user,
                    )[0]
                order.orderitems.remove(order_item)
                messages.info(request,"This item was removed from your cart.")
                return redirect("product:cart")
            else:
                messages.info(request, "This item has been removed from your cart")
                return redirect("product:cart")
        else:
            messages.info(request, "You do not have an active order")
            return redirect("product:cart")
        return redirect("product:cart")

class CartIncrementView(CreateView):
    model = Cart
    
    def get( self, request, pk, *args, **kwargs ):
        obj = get_object_or_404(Cart,pk=pk)
        #check if object in stock
        obj.quantity += 1
        obj.save()
        return redirect('product:cart')
    
class CartDecrementView(CreateView):
    model = Cart
    
    def get( self, request, pk, *args, **kwargs ):
        obj = get_object_or_404(Cart,pk=pk)
        #check if object in stock
        obj.quantity -= 1
        obj.save()
        return redirect('product:cart')
    
class SearchProduct(ListView):
    model = Product
    template_name = 'product/results.html'
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            object_list = self.model.objects.filter(name__icontains=query)
        else:
            object_list = self.model.objects.all()
        return object_list 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pro =  []
        for p in Product.objects.all():
            if p.discount > 0:
                pro.append(p)
        
        my_prod = Product.objects.filter(favourite=self.request.user)
        context["is_favourite"] = my_prod
        context["category"] = Category.objects.all() 
        context["object_list_5"] = Product.objects.all()[:5] 
        context["tags"] = Tag.objects.all() 
        context["product_discount"] = pro
        return context   