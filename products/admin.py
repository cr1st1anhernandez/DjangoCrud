from django.contrib import admin
from .models import Product, History, UserProfile, Sale, SaleItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'sku', 'price', 'quantity', 'created_at']
    search_fields = ['name', 'brand', 'sku', 'barcode']
    list_filter = ['category', 'gender', 'created_at']

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


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0
    readonly_fields = ['product_name', 'product_brand', 'product_sku', 'quantity', 'unit_price', 'subtotal']


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['ticket_number', 'user', 'total', 'created_at']
    list_filter = ['created_at', 'user']
    search_fields = ['ticket_number', 'user__username']
    readonly_fields = ['ticket_number', 'created_at']
    inlines = [SaleItemInline]


@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ['sale', 'product_name', 'product_brand', 'quantity', 'unit_price', 'subtotal']
    list_filter = ['sale__created_at']
    search_fields = ['product_name', 'product_brand', 'product_sku']
