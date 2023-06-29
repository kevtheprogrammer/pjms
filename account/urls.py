from django.urls import path,include
from django.contrib.auth.decorators import login_required

from .views import *

app_name = 'account'

urlpatterns = [
    # path("signup/", SignUpView.as_view(),name="signup"),
    # path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('',login_required(AdminIndexView.as_view()),name='dashboard'),
    path('customers/', login_required(CustomerListView.as_view()), name='customers'),
    path('products/', login_required(ProductListView.as_view()), name='products'),
    path('products/<int:pk>/<str:slug>/', login_required(ProductDetailView.as_view()), name='product-detail'),
    path('orders/', login_required(OrderListView.as_view()), name='orders'),
    path('stock/', login_required(StockListView.as_view()), name='stock'),
    path('orders/<int:pk>/', login_required(OrderDetailView.as_view()), name='order-detail'),
    path('stock/<int:pk>/', login_required(StockDetailView.as_view()), name='stock-details'),
    
]

 
 