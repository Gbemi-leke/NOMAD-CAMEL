from django.contrib import admin

from frontend.models import *

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_active', 'created_at']
    inlines = [ProductImageInline, ProductSizeInline]

admin.site.register(ProductImage)
admin.site.register(ProductSize)
