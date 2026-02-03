from django.contrib import admin
from .models import User, Society

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'contact_no', 'society', 'created_at')

admin.site.register(User,UserAdmin)
admin.site.register(Society)