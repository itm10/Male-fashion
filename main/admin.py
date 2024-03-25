from django.contrib import admin
from .models import Product, Images, Shoppingcart
from modeltranslation.admin import TranslationAdmin


@admin.register(Product)
class ProductAdmin(TranslationAdmin):
    list_display = ('product_name', )


admin.site.register((Images, Shoppingcart))

