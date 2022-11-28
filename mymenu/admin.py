from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display = ('full_name',)
admin.site.register(Admin, UserAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(Category, CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category',)
admin.site.register(Product, ProductAdmin)