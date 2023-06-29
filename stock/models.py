from django.db import models
from django.urls import reverse

from account.models import User
from product.models import Product

class StockModel(models.Model):
    prod        = models.ForeignKey(Product, on_delete=models.CASCADE,related_name="product",verbose_name="product")
    quantity    = models.IntegerField(default=1)
    updated     = models.DateField( auto_now=True )
    timestamp   = models.DateField( auto_now_add=True )
    slug        = models.SlugField( default=None )
    #  need to remove slug
    #def get_stock_leve --> low, hight, mediu


    def __str__(self):
        return f'{self.prod} stock' 

    def __unicode__(self):
        return f'{self.prod} stock' 
     
    def get_absolute_url(self):   
        return reverse('account:stock-details', args=[self.pk])
     
     
    class Meta:
	    ordering = ['-updated']


