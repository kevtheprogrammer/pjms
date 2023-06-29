from django.contrib import admin


from .models import *

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ( 'title', 'updated', )
    search_fields = ( 'title', ) 
 

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount','description',  )
    search_fields = ('name', 'price', 'description' ,) 
    list_filter = ('category', 'author__email','price','updated',)

     
    actions = [ 'publish', 'draft' ]
    
    def publish(self, queryset):
        queryset.update(is_pub=True)
        
    def draft(self, queryset):
        queryset.update(is_pub=False)
    
    
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ( 'item', 'quantity','updated', )
    list_filter = ('updated',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ( 'status', 'client','ordered','shipping_fee', )
    search_fields = ( 'client.email', ) 
    list_filter = ('updated','status')
 
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ( 'title', 'timestamp', )
    search_fields = ( 'title', ) 
 
 
