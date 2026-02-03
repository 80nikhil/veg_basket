from django.contrib import admin
from .models import Product, Order, OrderItem

# admin.site.register(Product)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'customer_phone', 'total_amount', 'status', 'created_at']
    inlines = [OrderItemInline]