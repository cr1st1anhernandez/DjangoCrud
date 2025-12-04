from django.contrib import admin
from .models import Product, History, UserProfile

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'price', 'quantity', 'created_at']
    search_fields = ['name', 'sku']
    list_filter = ['created_at']

@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'product_name', 'action', 'timestamp']
    list_filter = ['action', 'timestamp', 'user']
    search_fields = ['product_name', 'user__username']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_admin']
    list_filter = ['is_admin']
    search_fields = ['user__username']
