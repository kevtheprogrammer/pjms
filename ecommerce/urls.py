from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.decorators import login_required
from account.views import AdminIndexView

from product.views import SearchProduct, ShopListView,AboutUsView,HomeListView

urlpatterns = [
    path("", HomeListView.as_view(),name='home'),
    path("admin/", admin.site.urls),
    path("product/", include('product.urls')),
    path("about/", AboutUsView.as_view(),name='about'),
    path("shop/", ShopListView.as_view(),name='shop'),
    path("auth/", include('django.contrib.auth.urls')),
    path("search/results/", SearchProduct.as_view(),name='search'),
    path('dash/',include('account.urls')),
    path('payment/',include('payment.urls')),
    path('paypal/', include('paypal.standard.ipn.urls')),
]



urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)
