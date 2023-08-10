from django.contrib import admin
from .models import *


# Register your models here.


class ItemInline(admin.TabularInline):
    model = ItemOrder
    readonly_fields = ['user', 'product', 'variant', 'size', 'color', 'quantity', 'price']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'email', 'first_name', 'last_name', 'address', 'create', 'paid', 'get_price', 'code']
    inlines = [ItemInline]


class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'start', 'end', 'discount', 'active']


admin.site.register(Order, OrderAdmin)
admin.site.register(ItemOrder)
admin.site.register(Coupon,CouponAdmin)
