from django.contrib import admin

from frontend.models import *

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'is_active', 'created_at']
    inlines = [ProductImageInline]

admin.site.register(ProductImage)

