from django.contrib import admin
from .models import Category, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name_prod', 'grade')
    list_filter = ('name_prod', 'categories',)
    ordering = ('name_prod', )
    search_fields = ('name_prod', 'grade', 'categories')
    prepopulated_fields = {"slug": ("name_prod",)}


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
