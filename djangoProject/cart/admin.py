from django.contrib import admin
from .models import *


# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'variant', 'quantity']


class CompareAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'session_key']


admin.site.register(Cart, CartAdmin)
admin.site.register(Compare, CompareAdmin)
