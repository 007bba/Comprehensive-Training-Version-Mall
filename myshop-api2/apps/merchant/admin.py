from django.contrib import admin
from .models import Shop


@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'merchant', 'status', 'create_time', 'update_time')
    list_filter = ('status',)
    search_fields = ('name',)
