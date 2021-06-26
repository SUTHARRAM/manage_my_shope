from django.contrib import admin

from .models import Stock, Category

from .forms import StockCreateForm

class StockCreateAdmin(admin.ModelAdmin):
    ''' This will display all the content in specified manner '''
    list_display = ['category', 'item_name', 'quantity']
    form = StockCreateForm
    list_filter = ['category']
    search_fields = ['category', 'item_name']

admin.site.register(Stock, StockCreateAdmin)
admin.site.register(Category)
