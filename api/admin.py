from django.contrib import admin
from . models import *

@admin.register(User)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ('username', 'email_id', 'password','role')
    list_filter = ('role','society','city')
    search_fields = ('contact_no','username','role')
admin.site.register(Society)
admin.site.register(Category)
admin.site.register(Unit)
admin.site.register(Product)
admin.site.register(FlashSale)
admin.site.register(Order)
admin.site.register(OrderProduct)
admin.site.register(address)
admin.site.register(City)
admin.site.register(Aids_banner)
admin.site.register(Settings)
admin.site.register(SlotMaster)
admin.site.register(EliminatedSlot)