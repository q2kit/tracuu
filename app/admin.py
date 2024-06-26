from django.contrib import admin
from app.models import Product


class ProductAdmin(admin.ModelAdmin):
    search_fields = ['tax_code', 'product_name']
    list_display = ['tax_code', 'product_name', 'created_at']


admin.site.register(Product, ProductAdmin)

admin.site.site_header = 'Quốc Anh TH'
admin.site.site_title = 'Quốc Anh TH'
