from django.contrib import admin
from .models import ProductCategory, Product, CustomerProduct, ProductRecall

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'model_number', 'manufacturer', 'category']
    list_filter = ['category']
    search_fields = ['name', 'model_number']
    autocomplete_fields = ['manufacturer', 'category']


@admin.register(CustomerProduct)
class CustomerProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'customer', 'serial_number', 'purchase_date']
    list_filter = ['purchase_date']
    search_fields = ['serial_number', 'customer__email', 'product__name']
    autocomplete_fields = ['product', 'customer']


@admin.register(ProductRecall)
class ProductRecallAdmin(admin.ModelAdmin):
    list_display = ['product', 'initiated_by', 'date_initiated', 'is_active']
    list_filter = ['is_active', 'date_initiated']
    search_fields = ['product__name', 'initiated_by__email']
    autocomplete_fields = ['product', 'initiated_by']
