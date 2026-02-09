from django.contrib import admin
# Use the one we just fixed!

# admin.site.register(Product)

from django.contrib import admin
from api.models import WalletHistory

@admin.register(WalletHistory)
class WalletHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'payment_type', 'performed_by', 'created_at')
    list_filter = ('payment_type', 'created_at')