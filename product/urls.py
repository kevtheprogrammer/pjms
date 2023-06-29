from django.contrib import admin
from django.urls import path

from django.contrib.auth.decorators import login_required

from .views import *

app_name = "product" 

urlpatterns = [
    path('<int:pk>/<str:slug>/', ProductDetailView.as_view(),name="detail"),
    path('cart/', login_required(CartView.as_view()),name="cart"),
    path('favourite/',login_required(FavouriteView.as_view()),name='favourite'),
    path('checkout/',login_required(CheckOutCreateView.as_view()),name='checkout'),
    path('remove-from-bookmark/<int:pk>/',login_required(FavouriteToggleView.as_view()),name='favourite-toggle'),
    path('add-to-cart/<int:pk>/',login_required(CartCreateView.as_view()),name='add-to-cart'),
    path('remove-from-cart/<int:pk>/',login_required(CartDeleteView.as_view()),name='remove-from-cart'),
    path('increment-quantity/<int:pk>/',login_required(CartIncrementView.as_view()),name='increment'),
    path('decrement-quantity/<int:pk>/',login_required(CartDecrementView.as_view()),name='decrement'),
]
