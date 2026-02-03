from django.contrib import admin
from .models import Category, Unit, Product,FlashSale

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')


# @admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'price', 'quantity', 'unit')


admin.site.register(Category,CategoryAdmin)
admin.site.register(Unit)
admin.site.register(Product, ProductAdmin)
admin.site.register(FlashSale)