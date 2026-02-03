from django.contrib import admin
from .models import UserCart, Order, OrderProduct

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'get_username', 'order_status', 'total_amount', 'created_at')
    list_filter = ('order_status', 'created_at')
    search_fields = ('order_id', 'user__username')
    inlines = [OrderProductInline]

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Customer'

@admin.register(UserCart)
class UserCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'is_order_checked_out')

admin.site.site_header = "VegBasket Admin"