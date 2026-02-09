from django.contrib import admin
from . models import *

admin.site.register(User)
admin.site.register(Society)
admin.site.register(Category)
admin.site.register(Unit)
admin.site.register(Product)
admin.site.register(FlashSale)
admin.site.register(Order)
admin.site.register(OrderProduct)
# Register your models here.
