from django.db import models
from django.urls import reverse

from account.models import User
from .managers import ProductManager

class Category(models.Model):
     cover			= models.ImageField(upload_to="category/cover/",default="category.png")
     title 			= models.CharField(max_length=700)
     timestamp 		= models.DateTimeField(auto_now_add=True)
     updated 		= models.DateTimeField(auto_now=True)
     slug			= models.SlugField(default=None)

     def __str__(self) -> str:
          return f'{self.title}'

     def get_absolute_url(self): 
          return reverse('product:category-details', args=[self.slug])
     
     class Meta:
	     ordering = ['-updated']


class Tag(models.Model):
     title 			= models.CharField(max_length=700)
     timestamp 		= models.DateTimeField(auto_now_add=True)
     updated 		= models.DateTimeField(auto_now=True)

     def __str__(self) -> str:
          return f'{self.title}'
 
class Product(models.Model):
     """products table"""
     thumb			= models.ImageField(upload_to="products/thum/",default="products.png")
     name 			= models.CharField(max_length=900)
     description 	     = models.TextField(verbose_name="product description")
     price 			= models.DecimalField(default=1.0,max_digits=1000,max_length=7,decimal_places=2)
     discount 		     = models.DecimalField(default=0.0,max_digits=1000,max_length=7,decimal_places=2) 
     is_pub			= models.BooleanField(default=False,verbose_name="is published")
     favourite 		= models.ManyToManyField(User, related_name='favourite', blank=True,default=None)
     category 		     = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="category",default=None)
     img1			     = models.ImageField(upload_to="products/thum/",blank=True,verbose_name="first image")
     img2			     = models.ImageField(upload_to="products/thum/",blank=True,verbose_name="second image")
     img3			     = models.ImageField(upload_to="products/thum/",blank=True,verbose_name="third image")
     tags 		     = models.ManyToManyField(Tag,related_name="tags")
     slug			     = models.SlugField(default=None)
     updated 		     = models.DateTimeField(auto_now=True)
     timestamp 		= models.DateTimeField(auto_now_add=True)
     author			= models.ForeignKey(User,on_delete=models.CASCADE,related_name="author",default=None)
     
     objects = ProductManager()

     

     def __str__(self):
          return f'{self.name}'
     
     def get_absolute_url(self):
          return reverse('product:detail',args=[self.pk,self.slug])
      
     def toggle_favourite(self):
          return reverse('product:favourite-toggle',args=[self.pk])
        
     def add_to_cart(self):
          return reverse('product:add-to-cart',args=[self.pk])
     
     def remove_from_cart(self):
          return reverse('product:remove-from-cart',args=[self.pk])
     
     def get_init_price(self):
          return self.price
     
     def get_discount_price(self):
          pri = self.get_init_price() - self.discount 
          return round(pri,2)
     
     def get_discount_percentage(self):
          prc = (  self.discount /self.get_init_price()) *    100 
          return round(prc,0)
     
     def get_absolute_url_admin(self):
          return reverse('account:product-detail',args=[self.pk,self.slug])
     
     class Meta:
	     ordering = ['-timestamp']

     #def 404_url
     #def out_of_stock_url
     #def get_price
     #def get_absolute_url
     #def get_discount
 
class Cart(models.Model):
     buyer 	     = models.ForeignKey(User, on_delete=models.CASCADE , default=None, related_name="buyer" ) 
     item 		= models.ForeignKey(Product, on_delete=models.CASCADE , default=None, related_name="item" )
     quantity 	     = models.IntegerField(default=1)
     timestamp 	= models.DateTimeField(auto_now_add=True)
     updated 		= models.DateTimeField(auto_now=True)
     
     #add object manager 


     def __str__(self):
          return f'{self.quantity} of {self.item}'
 
     def increment_quantity(self):
          return reverse('product:increment',args=[self.pk])
     
     def decrement_quantity(self):
         return reverse('product:decrement',args=[self.pk])
     
     def get_cost(self):
          pass
          # pr = getattr(self.item,'current_price')
          # if  pr and self.quantity >= 1:
          #      qs = pr() * self.quantity
          # return qs

     def get_cart_total(self):
          total_price = self.item.price *  self.quantity
          return total_price
     
     class Meta:
	     ordering = ['-updated']
            
class Order(models.Model):
     ORDER_STATUS_CHOICES= (
          ('Not Yet Shipped', 'Not Yet Shipped'),
          ('Shipped', 'Shipped'),
          ('Cancelled', 'Cancelled'),
          ('Refunded', 'Refunded'),
     )
     orderitems      = models.ManyToManyField(Cart, related_name="orderitems")
     client 		 = models.ForeignKey(User, on_delete=models.CASCADE,related_name="client")
     ordered 	      = models.BooleanField(default=False)
     status          = models.CharField(max_length=120, default='Not Yet Shipped', choices= ORDER_STATUS_CHOICES)
     shipping_fee    = models.DecimalField(default=8.00, max_digits=1000, decimal_places=2)
     email           = models.EmailField(max_length=111,blank=True,help_text="enter your active email")
     address         = models.CharField(max_length=400,blank=True,help_text="house no. or P.O.Box")
     city            = models.CharField(max_length=111,blank=True)
     state           = models.CharField(max_length=111,blank=True,help_text="province, country.")
     zip_code        = models.CharField(max_length=111,blank=True)
     timestamp 	 = models.DateTimeField(auto_now_add=True)
     updated 		 = models.DateTimeField(auto_now=True)

     #objects        = OrderManager()
    
      
     def __str__(self):
          return f"{self.client}'s order -  {self.status}"

     def is_refunded(self):
          if self.status == 'Refunded':
               return True
          return False
     
     def is_cancelled(self):
          if self.status == 'Cancelled':
               return True
          return False

     def is_not_shipped(self):
          if self.status == 'Not Yet Shipped':
               return True
          return False

     def is_shipped(self):
          if self.status == 'Shipped':
               return True
          return False
  
     def get_subtotal(self):
          subt = [int(x.get_cart_total()) for x in self.orderitems.all()] 
          return sum(subt)

     def view_order_url(self):
          return reverse('account:order-detail',args=[self.pk])
     
     class Meta:
	     ordering = ['-updated']

# class OrderRequst(models.Model):
#      ORDER_STATUS_CHOICES= (
#           ('Not Yet Shipped', 'Not Yet Shipped'),
#           ('Shipped', 'Shipped'),
#           ('Cancelled', 'Cancelled'),
#           ('Refunded', 'Refunded'),
#      )
#      orderitems      = models.ManyToManyField(Cart, related_name="orderitems")
#      client 		 = models.ForeignKey(User, on_delete=models.CASCADE,related_name="client")
#      ordered 	      = models.BooleanField(default=False)
#      status          = models.CharField(max_length=120, default='Not Yet Shipped', choices= ORDER_STATUS_CHOICES)
#      shipping_fee    = models.DecimalField(default=5.99, max_digits=100, decimal_places=2)
#      email           = models.EmailField(max_length=111,blank=True,help_text="enter your active email")
#      address         = models.CharField(max_length=400,blank=True,help_text="house no. or P.O.Box")
#      city            = models.CharField(max_length=111,blank=True)
#      state           = models.CharField(max_length=111,blank=True,help_text="province, country.")
#      zip_code        = models.CharField(max_length=111,blank=True)
#      timestamp 	 = models.DateTimeField(auto_now_add=True)
#      updated 		 = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f'{self.name}'

#     def __unicode__(self):
#         return f'{self.name}'


# class Rating(models.Model):
#      ratings = models.IntegerField(default=0)
#      review = models.IntegerField()
#      comment =  models.TextField()
#      prod = models.ForeignKey("product.Product", verbose_name="prod", on_delete=models.CASCADE)
#      user = models.ForeignKey("account.User", verbose_name="user", on_delete=models.CASCADE)

 