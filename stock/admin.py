from django.contrib import admin

from stock.models import StockModel

@admin.register(StockModel)
class StockModelAdmin(admin.ModelAdmin):
    list_display = ('prod','quantity', 'updated', )
 