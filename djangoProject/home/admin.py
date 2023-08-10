from django.contrib import admin
from .models import *
import admin_thumbnails


# Register your models here.
class ProductVariantsInlines(admin.TabularInline):
    model = Variants
    extra = 3


@admin_thumbnails.thumbnail('image')
class ImageInlines(admin.TabularInline):
    model = Images
    extra = 2


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'create', 'update')
    list_filter = ('create',)

    prepopulated_fields = {
        'slug': ('name',)
    }


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'create', 'update', 'amount', 'available', 'total_price', 'sell']
    list_filter = ('available',)

    change_list_template = 'home/change.html'
    # raw_id_fields = ('category',)
    inlines = [ProductVariantsInlines, ImageInlines]


class VariantAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


class SizeAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


class ColorAdmin(admin.ModelAdmin):
    list_display = ['name', 'id']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'create', 'rate']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Variants)
admin.site.register(Size, SizeAdmin)
admin.site.register(Color, ColorAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Images)
admin.site.register(Brand)
admin.site.register(Chart)
admin.site.register(Views)
admin.site.register(Gallery)
