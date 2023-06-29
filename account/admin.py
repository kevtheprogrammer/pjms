from django.contrib import admin

from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email','first_name', 'last_name','country',)
    search_fields = ('first_name','email','last_name') 
 
    actions = ['verify','unverify','activate' ,'deactivate' ]
    
    def verify(self, queryset):
        queryset.update(is_verified=True)
        
    def unverify(self, queryset):
        queryset.update(is_verified=False)
        
    def activate(self, queryset):
        queryset.update(is_active=True)
        
    def deactivate(self, queryset):
        queryset.update(is_active=False)
